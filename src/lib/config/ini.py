"""Config Loader"""
from configparser import ConfigParser, ExtendedInterpolation

from settings.ini import EXTENDED_INTERPOLATION


options = dict()

if EXTENDED_INTERPOLATION:
    options['interpolation'] = ExtendedInterpolation()

loader = ConfigParser(**options)


def load(path):
    return loader.read(path)


def parse(config):
    return loader.read_string(config)
