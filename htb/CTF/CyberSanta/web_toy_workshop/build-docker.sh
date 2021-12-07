#!/bin/bash
docker rm -f web_toy_workshop
docker build -t web_toy_workshop . 
docker run --name=web_toy_workshop --rm -p1337:1337 -it web_toy_workshop
