FROM node:12.13.0-alpine

# Install packages
RUN apk --no-cache add supervisor

# Setup app
RUN mkdir -p /app

# Add application
WORKDIR /app
COPY --chown=nobody challenge .

# Setup supervisor
COPY config/supervisord.conf /etc/supervisord.conf

RUN yarn

# Expose the port node-js is reachable on
EXPOSE 1337

# Copy entrypoint
COPY entrypoint.sh /entrypoint.sh

# Start the node-js application
ENTRYPOINT [ "/entrypoint.sh" ]
CMD ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]