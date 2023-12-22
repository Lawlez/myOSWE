#!/bin/bash
docker rm web_saturn
docker build -t web_saturn .
docker run --name=web_saturn -p 1337:1337 -it web_saturn
