#!/usr/bin/env python3
from pwn import *
import re, shlex, random, string, ssl
from urllib.parse import urlparse

#AUTH_HEADER = "Authorization: Bearer u5fgj5c4qmktx5u57hs2xxey44y6uslo" #rw
#AUTH_HEADER = "Authorization: Bearer ksu357m54yvaana7sao6icvohmmnlbou" #reaad

#AUTH_HEADER = "Authorization: Bearer fd2if2dwkgt5y4jyw6r474pwmn4i6p2x" #rw
AUTH_HEADER = "Authorization: Bearer ssss" #reaad

PROXY = ("localhost", 8080)
extracted_values = {}


def parse_curl_command(cmd):
    tokens = shlex.split(cmd)
    method = None
    headers = []
    form_fields = {}
    url = None
    i = 1  # skip 'curl'
    while i < len(tokens):
        token = tokens[i]
        if token == "-H":
            i += 1
            headers.append(tokens[i])
        elif token == "-F":
            i += 1
            field = tokens[i]
            if "=" in field:
                key, value = field.split("=", 1)
                form_fields[key] = value
        elif token == "-X":
            i += 1
            method = tokens[i]
        elif token.startswith("-"):
            pass
        else:
            url = tokens[i]
        i += 1
    if not method:
        method = "POST" if form_fields else "GET"
    return {
        "method": method,
        "headers": headers,
        "form_fields": form_fields,
        "url": url,
    }


def build_request(parsed):
    url = parsed["url"]
    for key, value in extracted_values.items():
        url = url.replace("{" + key + "}", value)
    parsed["url"] = url

    url_parts = urlparse(url)
    host = url_parts.hostname
    port = url_parts.port or (443 if url_parts.scheme == "https" else 80)
    path = url_parts.path or "/"
    if url_parts.query:
        path += "?" + url_parts.query

    method = parsed["method"]
    headers = {}
    for h in parsed["headers"]:
        if ":" in h:
            k, v = h.split(":", 1)
            headers[k.strip()] = v.strip()
    auth_key = AUTH_HEADER.split(":", 1)[0].strip()
    auth_val = AUTH_HEADER.split(":", 1)[1].strip()
    headers[auth_key] = auth_val
    headers["Host"] = host
    headers["User-Agent"] = "pwntools-http-client"

    body = ""
    if parsed["form_fields"]:
        boundary = "----WebKitFormBoundary" + "".join(
            random.choices(string.ascii_letters + string.digits, k=16)
        )
        headers["Content-Type"] = f"multipart/form-data; boundary={boundary}"
        parts = []
        for key, value in parsed["form_fields"].items():
            parts.append(
                f'--{boundary}\r\nContent-Disposition: form-data; name="{key}"\r\n\r\n{value}\r\n'
            )
        parts.append(f"--{boundary}--\r\n")
        body = "".join(parts)
        headers["Content-Length"] = str(len(body))

    if PROXY and url_parts.scheme == "http":
        req_line = f"{method} {url} HTTP/1.1"
    else:
        req_line = f"{method} {path} HTTP/1.1"
    req_lines = [req_line]
    for key, value in headers.items():
        req_lines.append(f"{key}: {value}")
    req_lines.append("")
    req_lines.append(body)
    request_str = "\r\n".join(req_lines)
    return request_str, host, port, url_parts.scheme


def send_request(request_str, host, port, scheme):
    if PROXY:
        p = remote(PROXY[0], PROXY[1])
        if scheme == "https":
            connect_cmd = f"CONNECT {host}:{port} HTTP/1.1\r\nHost: {host}\r\n\r\n"
            p.send(connect_cmd)
            resp = p.recvuntil(b"\r\n\r\n", timeout=5).decode()
            if "200" not in resp:
                log.error("Proxy CONNECT failed: " + resp)
                return None
            # Skip certificate verification using an unverified SSL context.
            context = ssl._create_unverified_context()
            p.sock = context.wrap_socket(p.sock, server_hostname=host)
    else:
        p = remote(host, port, ssl=(scheme == "https"))
    p.send(request_str)
    response = p.recvall(timeout=10).decode(errors="replace")
    return response


def execute_curl_command(cmd):
    parsed = parse_curl_command(cmd)
    req_str, host, port, scheme = build_request(parsed)
    log.info("Sending request:\n" + req_str)
    response = send_request(req_str, host, port, scheme)
    log.info("Received response:\n" + response)
    return response


def main():
    curl_commands = [
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/regions',
    
    # Servers:
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/servers',  # GET (extract server_uuid)
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/servers/{server_uuid}',
    'curl -i -H "$AUTH_HEADER" -X POST https://api.cloudscale.ch/v1/servers/{server_uuid}/reboot',
    'curl -i -H "$AUTH_HEADER" -X POST https://api.cloudscale.ch/v1/servers/{server_uuid}/start',
    'curl -i -H "$AUTH_HEADER" -X POST https://api.cloudscale.ch/v1/servers/{server_uuid}/stop',
    'curl -i -H "$AUTH_HEADER" -X PATCH -F flavor=flex-32-16 https://api.cloudscale.ch/v1/servers/{server_uuid}',
    'curl -i -H "$AUTH_HEADER" -X DELETE https://api.cloudscale.ch/v1/servers/{server_uuid}',
    
    # Server Groups:
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/server-groups',  # GET (extract server_group_uuid)
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/server-groups/{server_group_uuid}',
    'curl -i -H "$AUTH_HEADER" -F name="load balancers" -F zone=rma1 -F type="anti-affinity" https://api.cloudscale.ch/v1/server-groups',
    'curl -i -H "$AUTH_HEADER" -X PATCH -F name="current" https://api.cloudscale.ch/v1/server-groups/{server_group_uuid}',
    'curl -i -H "$AUTH_HEADER" -X DELETE https://api.cloudscale.ch/v1/server-groups/{server_group_uuid}',
    
    # Flavors & Images (no extraction needed)
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/flavors',
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/images',
    
    # Custom Images:
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/custom-images',  # GET (extract custom_image_uuid)
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/custom-images/{custom_image_uuid}',
    'curl -i -H "$AUTH_HEADER" -X PATCH -F name=second-name https://api.cloudscale.ch/v1/custom-images/{custom_image_uuid}',
    'curl -i -H "$AUTH_HEADER" -X DELETE https://api.cloudscale.ch/v1/custom-images/{custom_image_uuid}',
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/custom-images/import',
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/custom-images/import/{custom_image_uuid}',
    'curl -i -H "$AUTH_HEADER" -F url=https://s5ya8gw30vmdk5z5hs1ej9kpzg57t1hq.oastify.com/foo.raw -F name=my-foo -F zones=lpg1 -F slug=foo -F source_format=raw -F user_data_handling=pass-through https://api.cloudscale.ch/v1/custom-images/import',
    
    # Volumes:
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/volumes',  # GET (extract volume_uuid)
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/volumes/{volume_uuid}',
    'curl -i -H "$AUTH_HEADER" -F size_gb=150 -F name=my-volume-name -F zone=lpg1 -F type=ssd -F servers={server_uuid} https://api.cloudscale.ch/v1/volumes',
    'curl -i -H "$AUTH_HEADER" -F snapshot="351d461c-2333-455f-b788-db11bf0b4aa2" https://api.cloudscale.ch/v1/volumes/{volume_uuid}/revert',
    'curl -i -H "$AUTH_HEADER" -X PATCH -F size_gb=100 https://api.cloudscale.ch/v1/volumes/{volume_uuid}',
    'curl -i -H "$AUTH_HEADER" -X DELETE https://api.cloudscale.ch/v1/volumes/{volume_uuid}',
    
    # Volume Snapshots:
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/volume-snapshots',  # GET (extract volume_snapshot_uuid)
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/volume-snapshots/{volume_snapshot_uuid}',
    'curl -i -H "$AUTH_HEADER" -F name="pre-dist-upgrade" -F source_volume={volume_uuid} https://api.cloudscale.ch/v1/volume-snapshots',
    'curl -i -H "$AUTH_HEADER" -X PATCH -F name=new-name https://api.cloudscale.ch/v1/volume-snapshots/{volume_snapshot_uuid}',
    'curl -i -H "$AUTH_HEADER" -X DELETE https://api.cloudscale.ch/v1/volume-snapshots/{volume_snapshot_uuid}',
    
    # Floating IPs (using an IP address directly, so no placeholder here)
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/floating-ips',
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/floating-ips/192.0.2.123',
    'curl -i -H "$AUTH_HEADER" -F type=regional -F ip_version=6 -F region=lpg -F server={server_uuid} https://api.cloudscale.ch/v1/floating-ips',
    'curl -i -H "$AUTH_HEADER" -F server={server_uuid} https://api.cloudscale.ch/v1/floating-ips/192.0.2.123',
    'curl -i -H "$AUTH_HEADER" -X PATCH -F server={server_uuid} https://api.cloudscale.ch/v1/floating-ips/192.0.2.123',
    'curl -i -H "$AUTH_HEADER" -X DELETE https://api.cloudscale.ch/v1/floating-ips/192.0.2.123',
    
    # Networks:
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/networks',  # GET (extract network_uuid)
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/networks/{network_uuid}',
    'curl -i -H "$AUTH_HEADER" -F name=my-network-name -F zone=lpg1 -F mtu=9000 https://api.cloudscale.ch/v1/networks',
    'curl -i -H "$AUTH_HEADER" -X PATCH -F mtu=1500 https://api.cloudscale.ch/v1/networks/{network_uuid}',
    'curl -i -H "$AUTH_HEADER" -X DELETE https://api.cloudscale.ch/v1/networks/{network_uuid}',
    
    # Subnets:
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/subnets',  # GET (extract subnet_uuid)
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/subnets/{subnet_uuid}',
    'curl -i -H "$AUTH_HEADER" -H "Content-Type: application/json" --data "{ \\"cidr\\": \\"192.168.42.0/24\\", \\"network\\": \\"{network_uuid}\\"}" https://api.cloudscale.ch/v1/subnets',
    'curl -i -H "$AUTH_HEADER" -X DELETE https://api.cloudscale.ch/v1/subnets/{subnet_uuid}',
    
    # Load-balancers:
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/load-balancers',  # GET (extract lb_uuid)
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/load-balancers/{lb_uuid}',
    'curl -i -H "$AUTH_HEADER" -F name=web-lb -F flavor=lb-standard -F zone=lpg1 https://api.cloudscale.ch/v1/load-balancers',
    'curl -i -H "$AUTH_HEADER" -X PATCH -F name=web-lb https://api.cloudscale.ch/v1/load-balancers/{lb_uuid}',
    'curl -i -H "$AUTH_HEADER" -X DELETE https://api.cloudscale.ch/v1/load-balancers/{lb_uuid}',
    
    # LB Pools:
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/load-balancers/pools',  # GET (extract pool_uuid)
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/load-balancers/pools/{pool_uuid}',
    'curl -i -H "$AUTH_HEADER" -F name="swimming-pool" -F algorithm="round_robin" -F load_balancer="{lb_uuid}" -F protocol="tcp" https://api.cloudscale.ch/v1/load-balancers/pools',
    'curl -i -H "$AUTH_HEADER" -X PATCH -F name="new-name" https://api.cloudscale.ch/v1/load-balancers/pools/{pool_uuid}',
    #'curl -i -H "$AUTH_HEADER" -X DELETE https://api.cloudscale.ch/v1/load-balancers/pools/{pool_uuid}',
    
    # LB Pool Members:
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/load-balancers/pools/{pool_uuid}/members',  # GET (extract member_uuid)
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/load-balancers/pools/{pool_uuid}/members/{member_uuid}',
    'curl -i -H "$AUTH_HEADER" -F name="new-member" -F protocol_port="8080" -F address="10.11.12.3" -F subnet="70d282ab-2a01-4abb-ada5-34e56a5a7eee" https://api.cloudscale.ch/v1/load-balancers/pools/{pool_uuid}/members',
    'curl -i -H "$AUTH_HEADER" -X PATCH -F name="new-name" https://api.cloudscale.ch/v1/load-balancers/pools/{pool_uuid}/members/{member_uuid}',
    'curl -i -H "$AUTH_HEADER" -X DELETE https://api.cloudscale.ch/v1/load-balancers/pools/{pool_uuid}/members/{member_uuid}',
    
    # LB Listeners:
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/load-balancers/listeners',  # GET (extract listener_uuid)
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/load-balancers/listeners/{listener_uuid}',
    'curl -i -H "$AUTH_HEADER" -F name="new-listener" -F pool="{pool_uuid}" -F protocol="tcp" -F protocol_port=1337 https://api.cloudscale.ch/v1/load-balancers/listeners',
    'curl -i -H "$AUTH_HEADER" -X PATCH -F name="new-name" https://api.cloudscale.ch/v1/load-balancers/listeners/{listener_uuid}',
    'curl -i -H "$AUTH_HEADER" -X DELETE https://api.cloudscale.ch/v1/load-balancers/listeners/{listener_uuid}',
    
    # LB Health Monitors:
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/load-balancers/health-monitors',  # GET (extract hm_uuid)
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/load-balancers/health-monitors/{hm_uuid}',
    'curl -i -H "$AUTH_HEADER" -F pool="{lb_uuid}" -F type="tcp"  https://api.cloudscale.ch/v1/load-balancers/health-monitors',
    'curl -i -H "$AUTH_HEADER" -X PATCH -F delay_s=3 https://api.cloudscale.ch/v1/load-balancers/health-monitors/{hm_uuid}',
    'curl -i -H "$AUTH_HEADER" -X DELETE https://api.cloudscale.ch/v1/load-balancers/health-monitors/{hm_uuid}',
    
    # Objects Users:
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/objects-users',  # GET (extract object_user_uuid)
    'curl -i -H "$AUTH_HEADER" https://api.cloudscale.ch/v1/objects-users/{object_user_uuid}',
    'curl -i -H "$AUTH_HEADER" -F display_name=alan https://api.cloudscale.ch/v1/objects-users',
    'curl -i -H "$AUTH_HEADER" -X PATCH -F display_name=turing https://api.cloudscale.ch/v1/objects-users/{object_user_uuid}',
    'curl -i -H "$AUTH_HEADER" -X DELETE https://api.cloudscale.ch/v1/objects-users/{object_user_uuid}',
    
    # Metrics:
    'curl -i -H "$AUTH_HEADER" "https://api.cloudscale.ch/v1/metrics/buckets?start=2019-03-19&end=2019-03-20"'
]

    extraction_config = {
    1: {"pattern": r'"uuid":\s*"([^"]+)"', "placeholder": "server_uuid"},
    8: {"pattern": r'"uuid":\s*"([^"]+)"', "placeholder": "server_group_uuid"},
    15: {"pattern": r'"uuid":\s*"([^"]+)"', "placeholder": "custom_image_uuid"},
    22: {"pattern": r'"uuid":\s*"([^"]+)"', "placeholder": "volume_uuid"},
    28: {"pattern": r'"uuid":\s*"([^"]+)"', "placeholder": "volume_snapshot_uuid"},
    39: {"pattern": r'"uuid":\s*"([^"]+)"', "placeholder": "network_uuid"},
    44: {"pattern": r'"uuid":\s*"([^"]+)"', "placeholder": "subnet_uuid"},
    48: {"pattern": r'"uuid":\s*"([^"]+)"', "placeholder": "lb_uuid"},
    53: {"pattern": r'"uuid":\s*"([^"]+)"', "placeholder": "pool_uuid"},
    58: {"pattern": r'"uuid":\s*"([^"]+)"', "placeholder": "member_uuid"},
    63: {"pattern": r'"uuid":\s*"([^"]+)"', "placeholder": "listener_uuid"},
    68: {"pattern": r'"uuid":\s*"([^"]+)"', "placeholder": "hm_uuid"},
    73: {"pattern": r'"uuid":\s*"([^"]+)"', "placeholder": "object_user_uuid"}
}

    for i, cmd in enumerate(curl_commands):
        cmd = cmd.replace("$AUTH_HEADER", AUTH_HEADER)
        response = execute_curl_command(cmd)
        if i in extraction_config:
            cfg = extraction_config[i]
            match = re.search(cfg["pattern"], response)
            if match:
                extracted_values[cfg["placeholder"]] = match.group(1)
                log.info(f"Extracted {cfg['placeholder']}: {match.group(1)}")
            else:
                extracted_values[cfg["placeholder"]] = "NOTFOUND"
                log.warn(f"Failed to extract {cfg['placeholder']} from response.")


if __name__ == "__main__":
    context.log_level = "info"
    main()
