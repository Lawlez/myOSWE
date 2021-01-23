#!/usr/bin/python3
import socketserver
from Crypto.Cipher import AES
from Crypto.Util import Counter
import os

key = os.urandom(0x10).replace(b'\x00', b'\xff')
iv = os.urandom(0x10).replace(b'\x00', b'\xff')

def xor(a, b):
    return bytes([_a ^ _b for _a, _b in zip(a, b)])

def unhex(msg):
    return bytes.fromhex(msg)

def encrypt(data):
    ctr = Counter.new(128, initial_value=int(iv.hex(), 16))
    crypto = AES.new(key, AES.MODE_CTR, counter=ctr)
    if type(data) != bytes:
        data = data.encode()
    otp = os.urandom(len(data)).replace(b'\x00', b'\xff')
    return xor(crypto.encrypt(data), otp)

def decrypt(data):
    ctr = Counter.new(128, initial_value=int(iv.hex(), 16))
    crypto = AES.new(key, AES.MODE_CTR, counter=ctr)
    return crypto.decrypt(data.encode())

def get_flag():
    flag = open('flag.txt', 'r').read().strip()
    return encrypt(flag)

def send_msg(s, msg):
    s.send(msg.encode())

def get_input(s, msg):
    send_msg(s, msg)
    data = b''
    while (recv := s.recv(0x1000)) != b'':
        data += recv
        if data.endswith(b'\n'):
            break
    data = data.strip()
    return data.decode()

def main(s):
    while True:
        send_msg(s, '1) Get flag\n')
        send_msg(s, '2) Encrypt Message\n')
        send_msg(s, '3) Decrypt Message\n')
        try:
            opt = get_input(s, 'Your option: ')
            if opt == '1':
                send_msg(s, get_flag().hex()+'\n')
            elif opt == '2':
                pt = get_input(s, 'Enter plaintext: ')
                send_msg(s, encrypt(unhex(pt)).hex()+'\n')
            elif opt == '3':
                ct = get_input(s, 'Enter ciphertext: ')
                send_msg(s, decrypt(unhex(ct)).hex()+'\n')
            else:
                send_msg(s, 'Invalid option!\n')
        except:
            send_msg(s, 'An error occured.')
            return

class Handler(socketserver.BaseRequestHandler):
    def handle(self):
        main(self.request)

if __name__ == '__main__':
    socketserver.ThreadingTCPServer.allow_reuse_address = True
    server = socketserver.ThreadingTCPServer(('0.0.0.0', 1337), Handler)
    server.serve_forever()
