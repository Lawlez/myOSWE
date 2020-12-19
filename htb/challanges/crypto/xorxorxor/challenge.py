#!/usr/bin/python3
import os
flag = open('flag.txt', 'r').read().strip().encode()
output = bytes.fromhex(open('output.txt', 'r').read().strip())
#print(flag)
#print(output)
class XOR:
    def __init__(self):
        self.key = os.urandom(4)
        print('key: ', self.key)
    def encrypt(self, data: bytes) -> bytes:
        xored = b''
        for i in range(len(data)):
            #print('origByte:  ',bytes([data[i]]) )
            #print('xoredByte: ', bytes([data[i] ^ self.key[i % len(self.key)]]))
            #print(bytes([data[i] ^ self.key[i % 4]]))
            xored += bytes([data[i] ^ self.key[i % len(self.key)]])
        return xored
    def decrypt(self, data: bytes) -> bytes:
        return self.encrypt(data)

def main():
    global flag
    global output
    i = 1
    while i == 1:
        crypto = XOR()
        dec2 = crypto.decrypt(output)
        try:
            lol = dec2.decode('utf8')
            if lol.find('htb') == 0:
                print(lol)
                i = 2
    
                pass
            pass
        except Exception as e:
            pass
    pass    
        
    #crypto = XOR()
    #enc = crypto.encrypt(flag)
    #dec = crypto.decrypt(enc)
    #dec2 = crypto.decrypt(output)
    #print ('Flag:', enc)
    #print ('solve: ', dec)
    #print ('solve2: ', dec2)

if __name__ == '__main__':
    main()
