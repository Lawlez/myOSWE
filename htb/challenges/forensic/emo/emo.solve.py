# ints we extracted from the obfuscated powershell
psh = [186, 141, 228, 182, 177, 171, 229, 236, 239, 239, 239, 228, 181, 182, 171, 229, 234, 239, 239, 228, 185, 179, 190, 184, 229, 151, 139, 157, 164,
       235, 177, 239, 171, 183, 236, 141, 128, 187, 235, 134, 128, 158, 177, 176, 139, 183, 154, 173, 128, 175, 151, 238, 140, 183, 162, 228, 170, 173, 179, 229]

# I want to break the array into equal parts of chunks of 4 integers.
# We know we want a 4 character Key, so we should set N rows of len(psh)/4
psh_split = []
arr_len = len(psh)
keylen = 4
n = int(arr_len/keylen)
# Our Base list 15 rows of 4 elements
for r in range(0, n):
    psh_split.append([0 for c in range(0, keylen)])
# now populate the 2d array with the values from psh
x = 0
for i in range(0, n):
    for j in range(0, keylen):
        psh_split[i][j] = psh[x]
        x += 1