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
    update_request = kwargs.get('update_request')
    headers = f"""
    proxy_http_version {http_version};
    proxy_cache_bypass $http_upgrade;
    proxy_set_header X-Forwareded-For $proxy_add_x_forwarded_for;
    proxy_set_header Upgrade $http_upgrade;
    proxy_set_header Host $host;
    proxy_set_header X-Real-IP $remote_addr;
    """
    return f"""
location {'=' if strict_match else ''} /{prefix_value if prefix_value else ''} {{
    {headers if update_request else ''}
    proxy_pass {protocol}://{upstream}/{prefix_value if pass_prefix else ''};
}}
"""


def create_default_location(endpoint, protocol='https'):
    return f"""
location / {{
    proxy_pass {protocol}://{endpoint};
}}
"""


def create_service(name, context, **options):
    if 'prefix' not in context:
        context['prefix'] = dict(value=name)

    context['upstream'] = name or context.get('upstream')
    context['service_name'] = context.get('service_name') or name

    upstream = create_upstream(name, **context)
    location = create_location(update_request=options.get('update_request'),
                               **context)

    return upstream, location


def _join_all(proxy, locations, upstreams):
    static_upstreams = '\n'.join(upstreams)
    static_locations = '\n'.join(locations)
    static_server = create_server(proxy['port'],
                                  proxy['server']['name'],
                                  locations=static_locations)
    return static_server, static_upstreams


def proxy_conf(filename):
    configuration = yml.load(filename)
    return validation.validate_proxy(configuration.get('proxy')), configuration.get('services')


def from_containers(containers, filename):
    proxy, _ = proxy_conf(filename)
    update_request = proxy['update_request']
    locations = []
    upstreams = []

    for container in containers:
        service = validation.validate_service(container)
        upstream, location = create_service(service['service_name'],
                                            service,
                                            update_request=update_request)
        locations.append(location)
        upstreams.append(upstream)

    endpoint = proxy['to']['host']
    protocol = proxy['to']['protocol']
    default_location = create_default_location(endpoint,
                                               protocol=protocol)
    locations.append(default_location)

    return _join_all(proxy, locations, upstreams)


def load_configuration(filename):
    proxy, services = proxy_conf(filename)
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

    return _join_all(proxy, locations, upstreams)
