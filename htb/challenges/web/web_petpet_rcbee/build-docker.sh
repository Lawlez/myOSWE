#!/bin/bash
docker rm -f web_petpet_rcbee
docker build -t web_petpet_rcbee . && \
docker run --name=web_petpet_rcbee --rm -p1337:1337 -it web_petpet_rcbee