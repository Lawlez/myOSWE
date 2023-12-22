#!/bin/bash
docker build --tag=web_jscalc .
docker run -p 1337:1337 --rm --name=web_jscalc -it web_jscalc
