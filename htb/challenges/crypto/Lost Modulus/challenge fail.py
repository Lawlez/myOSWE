#!/usr/bin/python3
#from Crypto.Util.number import getPrime, long_to_bytes, inverse
from struct import pack

import os

flag = open('output.txt', 'r').read().strip().encode()

def isPrime(n):
    """isPrime(n:long) -> bool
    Return True if n is a prime number, False otherwise.
    """
    if n == 2:
        return True
    if n == 1 or n&1 == 0:
        return False
    return pow(2, n-1, n) == 1

def getRandomNumber(bits):
    """getRandomNumber(bits:int)
    Generate a random number with the specified number of bits
    """
    assert bits >= 0
    bytes = (bits+7)//8
    hex = '%0*x' % (2*bytes, bytes*8)
    return int(hex, 16)


def getPrime(bits):
    """getPrime(bits:int) -> long
    Generate a random prime number of approximately the specified bit length.
    """
    assert bits >= 10
    # there are better ways to randomize this
    x = getRandomNumber(bits-1) | 1
    while not isPrime(x):
        x = getRandomNumber(bits-1) | 1
    return x

def long_to_bytes(n, blocksize=0):
    """long_to_bytes(n:long, blocksize:int) : string
    Convert a long integer to a byte string.
    If optional blocksize is given and greater than zero, pad the front of the
    byte string with binary zeros so that the length is a multiple of
    blocksize.
    """
    # after much testing, this algorithm was deemed to be the fastest
    s = b''
    n = int(n)
    while n > 0:
        s = pack('>I', n & 0xffffffff) + s
        n = n >> 32
    # strip off leading zeros
    for i in range(len(s)):
        if s[i] != b'\000'[0]:
            break
    else:
        # only happens when n == 0
        s = b'\000'
        i = 0
    s = s[i:]
    # add back some pad bytes.  this could be done more efficiently w.r.t. the
    # de-padding being done above, but sigh...
    if blocksize > 0 and len(s) % blocksize:
        s = (blocksize - len(s) % blocksize) * b'\000' + s
    return s


def inverse(self, n):
    """Calculates the inverse of n mod self.n."""
    if n < 0 or n > self.n:
        raise ValueError("The number should be positive and smaller than n.")
    if n == 0:
        return 0
    # using the extended Euclidean algorithm
    lm, hm = 1, 0
    low, high = self.n, n
    while low > 1:
        r = high//low
        nm, new = hm-lm*r, high-low*r
        lm, low, hm, high = nm, new, lm, low
    return lm % self.n


class RSA:
    def __init__(self):
        self.p = getPrime(512)
        self.q = getPrime(512)
        self.e = 3
        self.n = self.p * self.q
        self.d = inverse(self.e, (self.p-1)*(self.q-1))

    def encrypt(self, data: bytes) -> bytes:
        pt = int(data.hex(), 16)
        ct = pow(pt, self.e, self.n)
        return long_to_bytes(ct)

    def decrypt(self, data: bytes) -> bytes:
        ct = int(data.hex(), 16)
        pt = pow(ct, self.d, self.n)
        return long_to_bytes(pt)


def main():
    print(getRandomNumber(512))
    print(getPrime(512))
    #crypto = RSA()
    #print('Flag:', crypto.encrypt(flag).hex())
    #print('Flag:', crypto.decrypt(flag).hex())

if __name__ == '__main__':
    main()
