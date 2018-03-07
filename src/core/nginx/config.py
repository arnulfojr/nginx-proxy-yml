from lib.config import yml

from . import validation


def create_upstream(name, service_name, port, **kwargs):
    return f"""
upstream {name} {{
    server {service_name}:{port};
}}
"""


def create_server(port, name, locations=None):
    return f"""
server {{
    listen {port};
    server_name {name};
    {locations}
}}
"""


def create_location(prefix, upstream, protocol='http',
                    http_version='1.1', strict_match=True, **kwargs):
    prefix_value = prefix.get('value')
    pass_prefix = prefix.get('pass_prefix')
    return f"""
location {'=' if strict_match else ''} /{prefix_value if prefix_value else ''} {{
    proxy_http_version {http_version};
    proxy_cache_bypass $http_upgrade;
    proxy_set_header X-Forwareded-For $proxy_add_x_forwarded_for;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_pass {protocol}://{upstream}/{prefix_value if pass_prefix else ''};
}}
"""


def create_default_location(endpoint, protocol='https'):
    return f"""
location / {{
    proxy_pass {protocol}://{endpoint};
}}
"""


def create_service(name, context):
    if 'prefix' not in context:
        context['prefix'] = dict(value=name)

    context['upstream'] = context.get('upstream') or name

    upstream = create_upstream(context['upstream'], name, **context)
    location = create_location(**context)

    return upstream, location


def load_configuration(filename):
    configuration = yml.load(filename)

    proxy = validation.validate_proxy(configuration.get('proxy'))
    services = configuration.get('services')
    names = services.keys()

    locations = []
    upstreams = []
    for name in names:
        service = services[name]
        validation.validate_service(service)
        upstream, location = create_service(name, service)
        upstreams.append(upstream)
        locations.append(location)

    endpoint = proxy['to']['host']
    protocol = proxy['to']['protocol']
    default_location = create_default_location(endpoint, protocol=protocol)
    locations.append(default_location)

    static_locations = '\n'.join(locations)
    static_upstreams = '\n'.join(upstreams)

    static_server = create_server(proxy['port'], proxy['server']['name'],
                                  locations=static_locations)

    return static_server, static_upstreams
