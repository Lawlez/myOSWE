from Crypto.Cipher import DES
from Crypto.Hash import MD5
from Crypto.Protocol.KDF import PBKDF1
import base64
import sys

# script intended to decrypt wicket encryption using default pass
PASSWORD = b"WiCkEt-FRAMEwork"  #WiCkEt-CrYpT
SALT = b"12345678"  # Change this to the salt used in encryption
ITERATIONS = 1000


def decrypt_wicket_data(encrypted_data):
    try:
        # Decode the Base64 encoded data
        encrypted_data_bytes = base64.b64decode(encrypted_data)

        # Generate the encryption key using PBKDF1
        key = PBKDF1(PASSWORD, SALT, dkLen=8, count=ITERATIONS, hashAlgo=MD5)

        # Extract the initialization vector (IV) and ciphertext
        iv = encrypted_data_bytes[:8]
        ciphertext = encrypted_data_bytes[8:]

        # Create a DES cipher object
        des = DES.new(key, DES.MODE_CBC, iv)

        # Decrypt the ciphertext
        decrypted_data = des.decrypt(ciphertext)

        # Unpad the decrypted data (removing PKCS#5 padding)
        pad_len = decrypted_data[-1]
        decrypted_data = decrypted_data[:-pad_len]

        return decrypted_data.decode('utf-8')
    except Exception as e:
        print(f"Error during decryption: {e}")
        return None


if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python wicketDecrypt.py <encrypted_data>")
        sys.exit(1)

    encrypted_data = sys.argv[1]
    decrypted_data = decrypt_wicket_data(encrypted_data)
    if decrypted_data:
        print(f"Decrypted data: {decrypted_data}")
    else:
        print("Failed to decrypt data.")
