# TODO: Check if there is a newer version
FROM nginx:1.23.3-alpine

RUN rm /etc/nginx/conf.d/default.conf

# Copy our custom configuration to default.conf location in container
COPY ./default.conf /etc/nginx/conf.d/default.conf