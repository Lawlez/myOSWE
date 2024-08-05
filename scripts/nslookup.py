import subprocess
import re
import json
from ipwhois import IPWhois
from ipwhois.exceptions import IPDefinedError

def nslookup(host):
    try:
        result = subprocess.run(['nslookup', host], capture_output=True, text=True)
        return result.stdout
    except Exception as e:
        return str(e)

def whois(ip):
    try:
        obj = IPWhois(ip)
        result = obj.lookup_rdap()
        return result
    except IPDefinedError as e:
        return str(e)
    except Exception as e:
        return str(e)

def extract_ips(nslookup_output):
    # Regex pattern to match IP addresses specifically after "Name:"
    ip_pattern = re.compile(r'Name:\s+\S+\s+Address:\s+(\d+\.\d+\.\d+\.\d+)')
    return ip_pattern.findall(nslookup_output)

def clean_json(data):
    if isinstance(data, dict):
        return {k: clean_json(v) for k, v in data.items() if v and k not in ["notices", "links"] and clean_json(v) != {}}
    elif isinstance(data, list):
        return [clean_json(v) for v in data if v and clean_json(v) != []]
    else:
        return data

def compact_json(data, indent=0):
    if isinstance(data, dict):
        items = []
        for k, v in data.items():
            formatted_value = compact_json(v, indent + 4)
            items.append(f'"{k}": {formatted_value}')
        return '{ ' + ', '.join(items) + ' }'
    elif isinstance(data, list):
        items = [compact_json(item, indent + 4) for item in data]
        return '[ ' + ', '.join(items) + ' ]'
    else:
        return json.dumps(data)

def main():
    # Replace 'hosts.txt' with the path to your file containing the list of hosts
    with open('hosts.txt', 'r') as file:
        hosts = file.readlines()
    
    for host in hosts:
        host = host.strip()
        if host:
            print(f"NSLookup results for {host}:")
            nslookup_output = nslookup(host)
            print(nslookup_output)
            
            ips = extract_ips(nslookup_output)
            for ip in ips:
                print(f"Whois results for {ip}:")
                whois_info = whois(ip)
                cleaned_whois_info = clean_json(whois_info)
                formatted_whois_info = compact_json(cleaned_whois_info)
                print(formatted_whois_info)
                print("-" * 80)

if __name__ == "__main__":
    main()
