FROM ruby:2.7.5-alpine3.15

# Install supervisor
RUN apk add --update --no-cache supervisor

# Setup user
RUN adduser -D -u 1000 -g 1000 -s /bin/sh www

# Copy challenge files
RUN mkdir /app
COPY challenge/ /app
COPY config/supervisord.conf /etc/supervisord.conf

# Install dependencies
WORKDIR /app
RUN bundle install
RUN gem install shotgun

# Expose the app port
EXPOSE 1337

# Start supervisord
ENTRYPOINT ["/usr/bin/supervisord", "-c", "/etc/supervisord.conf"]