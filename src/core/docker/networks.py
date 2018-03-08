from lib.docker import client
from settings.docker import HOSTNAME


def all(driver='bridge'):
    return client.networks.list(filters={'driver': driver})


def get(network_id):
    return client.networks.get(network_id)


def get_containers_from(network_id):
    network = get(network_id)
    if network:
        return network.containers
    return None


def get_current():
    """Returns the first network occurrance"""
    me = client.containers.get(HOSTNAME)
    nets = all()
    for net in nets:
        net.reload()
        if me in net.containers:
            return net, me
    return None, me
