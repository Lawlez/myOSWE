#!/bin/sh

./qemu-system-x86_64 \
    -nographic \
    -nodefaults \
    -netdev user,id=net,hostfwd=tcp:0.0.0.0:1337-:1337 \
    -device e1000,netdev=net \
    -monitor /dev/null \
    -serial stdio \
    -m 256 \
    -L ./bios \
    -device nftdrm \
    -kernel bzImage \
    -initrd initramfs.cpio.gz \
    -append "console=ttyS0 loglevel=3 oops=panic panic=-1 pti=on kaslr" \
    -cpu qemu64,+smep,+smap \
    -no-reboot
