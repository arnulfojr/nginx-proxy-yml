# Docker + Nginx + YAML

# Docker

To use this image, you would need to have an exisitng docker network. There's no requirement on the docker network to use, but for local development it is recommended to use `bridge`

To get started:

`docker network create local-network`

This command will create a docker network called `local-network`.
This is required as the this image is meant to be used as a container that is attached to an existing network.


# Services

## File Structure

```yaml
proxy:
  port: 80  # nginx's port
  to:
    protocol: https
    host: www.google.com  # host to redirect unmatched locations
  server:
    name: proxy-name  # value of server_name

services:
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

Example for prefixes:

* Requested URI: `/my-app/hello/`
  * `prefix: my-app` & `pass_prefix: False` the service will receive `/hello/`
  * `prefix: my-app` & `pass_prefix: True` the service will receive `/my-app/hello/`

# Contact
Arnulfo Solis
