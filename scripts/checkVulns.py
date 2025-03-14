#!/usr/bin/env python3
import urllib.request
import json
from urllib.parse import quote
from pwn import log  

'''
input format example: 
aiohappyeyeballs
2.4.0
aiohttp
3.10.11
aiosignal
1.3.1
'''

API_BASE = "https://api.deps.dev"
SYSTEM = "PYPI"

def get_advisory_keys(package, version):
    package_enc = quote(package, safe='')
    url = f"{API_BASE}/v3/systems/{SYSTEM}/packages/{package_enc}/versions/{version}"
    try:
        with urllib.request.urlopen(url) as response:
            data = response.read().decode('utf-8')
            obj = json.loads(data)
            return obj.get("advisoryKeys", [])
    except Exception as e:
        log.error(f"Error fetching {package} {version}: {e}")
        return []

def main():
    input_file = "input.txt"   
    output_file = "output.txt"

    with open(input_file, "r") as f:
        lines = [line.strip() for line in f if line.strip()]

    results = []
    for i in range(0, len(lines), 2):
        if i+1 >= len(lines):
            log.error(f"Missing version for package {lines[i]}")
            continue
        package = lines[i]
        version = lines[i+1]
        log.info(f"Processing {package} {version}")
        keys = get_advisory_keys(package, version)
        if keys:
            results.append((package, version, keys))

    with open(output_file, "w") as f:
        for package, version, keys in results:
            f.write(f"{package} {version}: {keys}\n")

    log.info(f"Results saved to {output_file}")

if __name__ == "__main__":
    main()
