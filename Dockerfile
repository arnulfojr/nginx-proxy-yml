FROM nginx:alpine

MAINTAINER Arnulfo Solis arnulfojr94@gmail.com

ENV PATH "/nginx-helper/bin:${PATH}"

# Docker socket config
ENV DOCKER_HOST "unix:///tmp/docker.sock"

# Add the python scripts
RUN apk add --no-cache python3-dev yaml
RUN python3 -m ensurepip && rm -r /usr/lib/python*/ensurepip

ADD ./requirements.txt /nginx-helper/requirements.txt
RUN pip3 install -r /nginx-helper/requirements.txt

# Add the project
ENV PYTHONPATH "/nginx-helper/src"
ADD ./src /nginx-helper/src
ADD ./bin /nginx-helper/bin

# Volume for the proxy configuration file
VOLUME /proxy.yml

EXPOSE 80 443

# Set up the docker-entrypoint
ADD ./docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["/bin/sh", "/docker-entrypoint.sh"]

CMD ["serve"]
