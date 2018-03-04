from lib.config import yml


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
    pass_prefix = kwargs.get('pass_prefix')
    return f"""
location {'=' if strict_match else ''} /{prefix} {{
    proxy_http_version {http_version};
    proxy_cache_bypass $http_upgrade;
    proxy_set_header X-Forwareded-For $proxy_add_x_forwarded_for;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    proxy_pass {protocol}://{upstream}/{prefix if pass_prefix else ''};
}}
"""


def create_service(name, context):
    if 'prefix' not in context:
        context['prefix'] = name

    context['upstream'] = context.get('upstream') or name

    upstream = create_upstream(context['upstream'], name, **context)
    location = create_location(**context)

    return upstream, location


def load_configuration(filename):
    configuration = yml.load(filename)

    services = configuration.get('services')
    names = services.keys()

    locations = []
    upstreams = []
    for name in names:
        service = services[name]
        upstream, location = create_service(name, service)
        upstreams.append(upstream)
        locations.append(location)

    static_locations = '\n'.join(locations)
    static_upstreams = '\n'.join(upstreams)

    proxy = configuration.get('proxy')

    static_server = create_server(proxy['port'], proxy['server']['name'],
                                  locations=static_locations)

    return static_server, static_upstreams
