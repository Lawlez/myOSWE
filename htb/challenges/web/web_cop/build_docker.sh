#!/bin/bash
docker build --tag=cop .
docker run -p 1337:1337 --rm --name=cop -it cop