#!/usr/bin/python
# a very bad bruteforcer
from pwn import *

import string
r = remote("crypto.chal.csaw.io",1578)
def fuzz():
    for i in range(100):
        r.recvuntil(": ")
        tmp = "A"*i
        r.sendline(tmp)
        data = r.recvuntil("\n")
        cookie = data[16:-1]
        print(len(tmp),"\t", cookie, len(cookie))
def blocks(x):
    element = []
    for i in x
    range(0,len(x),32):
        element.append(x[i:i+32])
    # print element
    return element
def check_cookie(packet):
    r.recvuntil(": ")
    r.sendline(packet)
    data = r.recvuntil("\n")
    # print data
    cookie = data[16:-1]
    return blocks(cookie)
flag = ""
for pos in range(32):
    for char in string.printable:
        b = '_'*(31-len(flag)) + flag + char + '_'*(31-len(flag))        
        data = check_cookie(brute)
        if (data[1]==data[3]):
            #print data
            flag += char
            print brute, flag, "\r"
            break
r.close()