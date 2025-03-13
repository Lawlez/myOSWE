#!/usr/bin/env python3
import json
import urllib.request
from pwn import log  # pwntools is very useful, right?

def search_in_blocklist(url, search_str):
    try:
        with urllib.request.urlopen(url) as response:
            content = response.read().decode('utf-8', errors='replace')
    except Exception as e:
        log.error(f"Error fetching {url}: {e}")
        return []
    # Search each line for the search_str (case insensitive)
    return [line for line in content.splitlines() if search_str.lower() in line.lower()]

def main():
    # Load your JSON data from filters.json
    with open("filters.json", "r") as f:
        data = json.load(f)
    
    search_str = input("Enter the string to search for: ").strip()
    if not search_str:
        log.error("No search string provided!")
        return
    
    for filter_obj in data.get("filters", []):
        url = filter_obj.get("downloadUrl")
        if not url:
            continue
        name = filter_obj.get("name", "Unnamed Filter")
        log.info(f"Searching in blocklist: {name}")
        matches = search_in_blocklist(url, search_str)
        if matches:
            log.info(f"Found {len(matches)} match(es) in {name}:")
            for line in matches:
                print(line)
        else:
            log.info(f"No matches found in {name}")
        print("-" * 40)

if __name__ == '__main__':
    main()
