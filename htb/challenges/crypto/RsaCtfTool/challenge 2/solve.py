#python2
n = int("0ad9e2ef0f29e82503c8c66fe09ca9c13ad6b242976b3880b7381a24e8e15242f3673cfbb72ce5b3b848c2f28c256562e9152cb72436aefaa0540d2d70538e819a98aaea1cf6ad40bffba01cd6ec0615df116d17e0ccf71106cc5dea1fcf258bad891030d62868b16a3d886b0094fefa6b57ed8289db833e039f04f5bf7766995e95abdb38cd14301d3a6417bcb8c3004f4220afbdfae6a25d439eea2f5ee52de7af2d90a548882132d23246d95cec3f350457511e04bf2486c317d51153473d014108715b548087940e71fc7d6c505a7250afd5fa04308ecd3957520cfa7b0d1fa7c04c16506d8f7c0bb1b53c47156b39b452b6f7bc69ea33d4bccae38e063a7104be77552ab40ee1122f462ca98080ace75324fab9e22caef466e643cb579593e268c144b54430ae4f405c873eb8e88a8bc39957a6deddae450b23ad59d4096f4c8a825fd22ce0080f7e5feb117822ac3911386197e242dbd5ec5c", 16)
d = int("02f14b24e0cbd074192e9d0141bbba1cf843b85b6e8c58ea2ec53bf1be653bd58403fef99396cd438b39d003ce156605088801743891cba99348b7ba16b7d1f13b6723121180a342e7cce8826995dfa096b937083ea1d66dfb95f7f1c1667f1bfd972998d4ba688993f1d3c89083d7113982c2999fa0b35a61c901a352a4a261fcd041a65524e7d0945c7d4022a147e0119e3116f741cec140e1517ad815b7b857179e17977aafcfb0e46755e723d7bcdc37ad260629eb5b905fdf5a9c34252159f1b4c468abe59ede7b7c55a7fd735cd39b25d3b4d4e6061388f530feebfdea75271c7285aa91cb532c28a8a90bedb70212f04b45ab065dc8686c39e8b35ee50238f31d912edf5d1993c0d61ace6c56788cd27338baa7a6ce5ae07c98edcf76747ff54053cd840c5f78864f912d651f4a52d45c04f4ef82d5fb4b2605a0526bac8ee910a9c368ffe7afabe97ee961d6a535648211950a7a6efaf7f9",16)

c0 = 72692391911894820239191189364123919118920239191189171232869239191189239191189239191189100842391911894887239191189111239191189239191189239191189239191189172391911897710 



## try 1
plain = str(hex(pow(c0, d, n)))[2::]
print(''.join([chr(int(''.join(c0), 16)) for c0 in zip(plain[0::2],plain[1::2])]))

ciphertexts = [c0]
result = []
for ct in ciphertexts:
	pt = pow(ct,d,n)
	pt = str(hex(pow(ct, d, n)))[2::]
	result2 = ''.join([chr(int(''.join(c), 16)) for c in zip(pt[0::2],pt[1::2])])
	result.append(result2)
result_final = ''.join(result)
print("_______")
print(result_final)

## try 2

from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import padding

with open("./privatekey.pem", "rb") as key_file:
    print(key_file.read())
    private_key = serialization.load_pem_private_key(
        key_file.read(),
        password=None,
    )

    print(private_key)

    plaintext = private_key.decrypt(
        c0,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    print(plaintext)