# Docker + Nginx + YAML

## What is it?

The goal of this proxy is to attempt to `hijack` the traffic from services in the cloud by using a reverse proxy (namely, nginx).

![docker-overview](https://github.com/arnulfojr/nginx-proxy-yml/blob/docker-network/docs/network-overview.png)

> Note: Please do **not** use in production setups, this is purely meant to be used in development only.

# Getting Started

To use this image, you would need to have an exisitng docker network. There's no requirement on the docker network to use, but for local development it is recommended to use `bridge`.

To get started:

`docker network create local-network`

This command will create a docker network called `local-network`.
This is required as the this image is meant to be used as a container that is attached to an existing network.

The network arquirecture is as follows:

![docker-network](https://github.com/arnulfojr/nginx-proxy-yml/blob/docker-network/docs/docker-network.png)

Therefore, all the services have to be attached to a network.

## Services

### Defining through a file

In the root project a file named `proxy.yml` defines basics of the proxy configuration and basics of services (optional).

```yaml
proxy:
  port: 80  # nginx's port
  to:
    protocol: https
    host: www.google.com  # host to redirect unmatched locations
  server:
    name: proxy-name  # value of server_name

services:  # optional
  app:  # service name
    strict_match: True  # uses the '=' operator to match the location
    prefix:
      value: my-app
      pass_prefix: True  # if the prefix used in the location shall be passed to the proxied service
    protocol: http  # if HTTPS is required TLS/SSL is required + certs
    port: 5000  # container's port number
  another-app:  # service name
    # ...
```

### Definition through Docker

This image comes with dynamic discovery of services registered in a network.
This means that on container startup, the container will request the Docker API for the connected containers in the current network.

#### Requirements:

Although is easy to set up, some exclusion is sometimes wished.
So for the containers to be taken in consideration in the proxy's rules some docker labels need to be present.

* `local.proxy.pass_prefix`
  * `"true" || "false"`
* `local.application.port`
  * Container's exposed port
* `local.appliaction.name`
  * This will be used to name the `upstream`, the `prefix` and the `path` rule.

Example:

```yaml
# docker-compose.yml
services:
  app:
    networks:
      local-network:
        aliases:
          - my-app  # so we can use "my-app"
    labels:
      local.application.port: "8080"
      local.application.name: "my-app"
      local.proxy.pass_prefix: "true"
networks:
  local-network:
    external:
      name: local-network
```

This is the minimum set up in a `docker-compose.yml` file to set a service detected and registered in the proxy.

### Prefixes

Example for prefixes:

* Requested URI: `/my-app/hello/`
  * `prefix: my-app` & `pass_prefix: False` the service will receive `/hello/`
  * `prefix: my-app` & `pass_prefix: True` the service will receive `/my-app/hello/`


# Contact

* Arnulfo Solis
