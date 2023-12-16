# TODO: Check if there is a newer version
FROM nginx:1.23.3-alpine

RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom configuration to default.conf location in container
COPY ./default.conf /etc/nginx/conf.d/default.conf

# Since we don't have a command: instruction in the docker-compose file
# the normal behavior would be to have a CMD instruction here
# but apparently nginx image already already handles the starting, so we don't need it