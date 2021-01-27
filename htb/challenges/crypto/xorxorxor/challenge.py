#!/usr/bin/python3
import os
flag = open('flag.txt', 'r').read().strip().encode()
output = bytes.fromhex(open('output.txt', 'r').read().strip())
output2 = open('output.txt', 'r').read().strip()
output3 = bytes.fromhex('134af6e1297bc4a96f6a87fe046684e8047084ee046d84c5282dd7ef292dc9')
#print(flag)
print(output)
print(output2)
print(output3)
class XOR:
    def __init__(self):
        self.key = bytes.fromhex('5b1eb49a') #os.urandom(4)
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
    crypto = XOR()
    enc = crypto.encrypt(flag)
    print ('Flag:', enc.hex())

    i = 3
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

    dec = crypto.decrypt(bytes.fromhex(enc.hex()))
    dec2 = crypto.decrypt(output)
    #print ('Flag:', enc.hex())
    print ('solve: ', dec)
    print ('solve2: ', dec2)

if __name__ == '__main__':
    main()
