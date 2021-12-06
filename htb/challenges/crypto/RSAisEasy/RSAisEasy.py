#!/usr/bin/env python3
from Crypto.Util.number import bytes_to_long, getPrime
from secrets import flag1, flag2
from os import urandom

flag1 = bytes_to_long(flag1)
flag2 = bytes_to_long(flag2)

p, q, z = [getPrime(512) for i in range(3)]

e = 0x10001

n1 = p * q
n2 = q * z

c1 = pow(flag1, e, n1)
c2 = pow(flag2, e, n2)

E = bytes_to_long(urandom(69))

print(f'n1: {n1}')
print(f'c1: {c1}')
print(f'c2: {c2}')
print(f'(n1 * E) + n2: {n1 * E + n2}')
