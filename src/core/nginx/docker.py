
_PASS_PREFIX_LABEL = 'local.proxy.pass_prefix'

_APPLICATION_NAME_LABEL = 'local.application.name'

_APPLICATION_PROTOCOL_LABEL = 'local.application.protocol'

_APPLICATION_PORT_LABEL = 'local.application.port'


def transform_container(container):
    labels = container.labels
    pass_prefix = labels.get(_PASS_PREFIX_LABEL) == 'true'
    return {
        'strict_match': False,
        'prefix': {
            'value': labels.get(_APPLICATION_NAME_LABEL),
            'pass_prefix': pass_prefix
        },
        'protocol': labels.get(_APPLICATION_PROTOCOL_LABEL, 'http'),
        'upstream': labels.get(_APPLICATION_NAME_LABEL),
        'service_name': container.name,
        'port': int(labels.get(_APPLICATION_PORT_LABEL, 80))
    }


def transform(network, me=None):
    network.reload()

    def has_label(label, container):
        return container.labels.get(label) is not None
    
    containers = [transform_container(c)
                  for c in network.containers
                  if c != me and has_label(_APPLICATION_NAME_LABEL, c)]
    return containers

