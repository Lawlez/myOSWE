#!/bin/bash
docker build --tag=web_gunship .
docker run -p 1337:1337 --name=web_gunship --rm web_gunship