#!/bin/ash

# Secure entrypoint
chmod 600 /entrypoint.sh

# Generate random flag filename
FLAG=$(cat /dev/urandom | tr -dc 'a-zA-Z0-9' | fold -w 5 | head -n 1)
mv /app/flag /app/flag$FLAG

exec "$@"
