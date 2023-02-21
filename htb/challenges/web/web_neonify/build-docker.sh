docker build -t web_neonify .
docker run  --name=web_neonify --rm -p1337:1337 -it web_neonify