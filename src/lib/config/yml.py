import yaml


def load(path):
    with open(path) as config_file:
        data = yaml.load(config_file)
    return data
