
_APPLICATION_NAME = 'APPLICATION_NAME'

_APPLICATION_PROTOCOL = 'HOSTED_ZONE_PROTOCOL'

_APPLICATION_PORT = 'CONTAINER_PORT'

_ENV_VARS = frozenset((_APPLICATION_NAME,
                      _APPLICATION_PORT,
                      _APPLICATION_PROTOCOL))


def transform_container(container):
    env_vars = container.attrs['Config']['Env']
    variables = {}
    for env_var in env_vars:
        name, value = env_var.split('=')
        if name in _ENV_VARS:
            variables[name] = value
    return {
        'strict_match': False,
        'prefix': {
            'value': variables[_APPLICATION_NAME],
            'pass_prefix': True
        },
        'protocol': variables.get(_APPLICATION_PROTOCOL, 'http'),
        'upstream': variables[_APPLICATION_NAME],
        'service_name': container.name,
        'port': int(variables[_APPLICATION_PORT])
    }


def transform(network, me=None):
    network.reload()

    containers = [transform_container(c)
                  for c in network.containers
                  if c != me]
    return containers
