#!/bin/sh

docker build . -t pwn_nftdrm && \
docker run -it -p1337:1337 pwn_nftdrm
