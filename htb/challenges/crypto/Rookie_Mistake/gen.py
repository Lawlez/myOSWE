import os
from Crypto.Util.number import bytes_to_long, getPrime
from sympy import *
from secret import flag

flag1 = bytes_to_long(flag[:len(flag)//2] + os.urandom(69))
flag2 = bytes_to_long(flag[len(flag)//2:] + os.urandom(200))

def genprime():
    p = 2
    while p.bit_length() < 1020:
        p *= getPrime(30)
    while True:
        x = getPrime(16)
        if isprime((p * x) + 1):
            return (p * x) + 1
            break
      
p,q = [genprime() for _ in range(2)]

print("-" * 10 + "RSA PART" + "-" * 10)

e = 0x69420
ct1 = pow(flag1,e,p)

print(f'p: {hex(p)}')
print(f'e: {hex(e)}')
print(f'ct: {hex(ct1)}')

print("-" * 10 + "DH PART" + "-" * 10)

n = p * q
g = 0x69420
ct2 = pow(g, flag2, n)

print(f'n: {hex(n)}')
print(f'g: {hex(g)}')
print(f'ct: {hex(ct2)}')
