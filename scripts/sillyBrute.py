from Crypto.Cipher import AES
import base64

def brute_force_aes_ecb(ciphertext, known_plaintext):
    key_length = 16  # Assuming a 128-bit (16-byte) key length

    for i in range(256**key_length):
        print("trying")
        #generate key candidate
        key_candidate = i.to_bytes(key_length, 'big')
        #create AES cipher object with ECB mode
        cipher = AES.new(key_candidate, AES.MODE_ECB)

        # Decrypt the ciphertext using the key candidate
        decrypted = cipher.decrypt(ciphertext)

        # Check if the decrypted plaintext matches the known plaintext
        if decrypted == known_plaintext:
            print(key_candidate)
            return key_candidate

    return None
# {"usrid":1, "name":"guest                      {"}
# Example usage
known_plaintext = b'{"usrid":2, "name":"guest"}'  # known plaintext
ciphertext = base64.b64decode('sC3ZkdpTquf5pF28mrygZ1wClfk7OeGwT8PCtU/kjpw=')  #base64-encoded ciphertext

key = brute_force_aes_ecb(ciphertext, known_plaintext)
if key:
    print(f"Key found: {key.hex()}")
else:
    print("Key not found.")