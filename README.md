# Docker + Nginx + YAML

# Services

## File Structure

```yaml
proxy:
  port: 80  # nginx's port
  server:
    name: proxy-name  # value of server_name

services:
  app:  # service name
    strict_match: True  # uses the '=' operator to match the location
    upstream: my-apps-upstream  # optional: upstream name (if absent uses the service name)
    prefix: my-app
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
