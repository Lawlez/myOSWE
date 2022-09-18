#!/bin/bash
docker rm -f web_blinkerfluids
docker build -t web_blinkerfluids .
docker run --name=web_blinkerfluids --rm -p1337:1337 -it web_blinkerfluids
