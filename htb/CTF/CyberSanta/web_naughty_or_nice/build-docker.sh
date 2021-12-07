#!/bin/bash
docker build -t naughty_or_nice .
docker run  --name=naughty_or_nice --rm -p1337:1337 -it naughty_or_nice
