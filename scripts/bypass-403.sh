curl http://lwlx.xyz  ## => 403

## bypass 403 with xclient-ip
curl https://lwlx.xyz -H "X-Client-IP: 127.0.0.1" ## => redirect to another page ?

# This can work with multiple headers here is a list:

# X-Forwarded-Host
# X-Forwarded-For
# X-Client-IP