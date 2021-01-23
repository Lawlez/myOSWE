#!/usr/bin/python3
import os
output = bytes.fromhex(open('output.txt', 'r').read().strip()) 
print('input: ', output)
class XOR:
    def __init__(self):
        self.key = bytes.fromhex('5b1eb49a') #os.urandom(4)
        print('key: ', self.key)
    def decrypt(self, data: bytes) -> bytes:
        xored = b'' #0x0000005
        for i in range(len(data)):
            xored += bytes([data[i] ^ self.key[i % len(self.key)]]) 
        return xored

def main():
    global flag
    global output
    crypto = XOR()
    dec2 = crypto.decrypt(output)
    print ('Flag: ', dec2)

if __name__ == '__main__':
    main()
