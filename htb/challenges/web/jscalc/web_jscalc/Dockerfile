FROM node:alpine

# Install packages
RUN apk add --update --no-cache supervisor g++ make python3

# Setup app
RUN mkdir -p /app

# Add application
WORKDIR /app
COPY challenge .

# Add flag
COPY flag.txt /

# Install dependencies
RUN npm install

# Setup superivsord
COPY config/supervisord.conf /etc/supervisord.conf

# Expose the port node-js is reachable on
EXPOSE 1337

# Start the node-js application
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]