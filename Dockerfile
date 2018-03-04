FROM nginx:alpine

MAINTAINER Arnulfo Solis arnulfojr94@gmail.com

ENV PATH "/nginx-helper/bin:${PATH}"

# Add the python scripts
RUN apk add --no-cache python3 yaml

RUN python3 -m ensurepip && rm -r /usr/lib/python*/ensurepip

ADD ./requirements.txt /nginx-helper/requirements.txt

RUN pip3 install -r /nginx-helper/requirements.txt

ADD ./src /nginx-helper/src
ADD ./bin /nginx-helper/bin

ENV PYTHONPATH "/nginx-helper/src"

# Set up the docker-entrypoint
ADD ./docker-entrypoint.sh /docker-entrypoint.sh

ENTRYPOINT ["/bin/sh", "/docker-entrypoint.sh"]

CMD ["serve"]
