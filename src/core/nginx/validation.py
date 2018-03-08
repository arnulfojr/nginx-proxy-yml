from cerberus import Validator, DocumentError

from core import exc


PROTOCOLS = ('http', 'https')

_PROXY_SCHEMA = {
    'port': {
        'type': 'integer',
        'required': False,
        'empty': False,
        'default': 80
    },
    'update_request': {
        'type': 'boolean',
        'required': False,
        'empty': False,
        'default': False
    },
    'to': {
        'type': 'dict',
        'required': True,
        'empty': False,
        'schema': {
            'protocol': {
                'type': 'string',
                'allowed': PROTOCOLS,
                'default': 'http',
                'empty': False
            },
            'host': {
                'type': 'string',
                'empty': False,
                'required': True
            }
        }
    },
    'server': {
        'type': 'dict',
        'required': True,
        'empty': False,
        'schema': {
            'name': {
                'type': 'string',
                'required': True,
                'empty': False
            }
        }
    }
}

_PREFIX_SCHEMA = {
    'value': {
        'type': 'string',
        'required': False
    },
    'pass_prefix': {
        'type': 'boolean',
        'default': True,
        'empty': False,
        'required': True
    }
}

_SERVICES_SCHEMA = {
    'strict_match': {
        'type': 'boolean',
        'default': False,
        'empty': False
    },
    'prefix': {
        'type': 'dict',
        'schema': _PREFIX_SCHEMA,
        'required': True,
        'empty': False
    },
    'protocol': {
        'type': 'string',
        'allowed': PROTOCOLS,
        'default': 'http',
        'required': True,
        'empty': False
    },
    'port': {
        'type': 'integer',
        'default': 80,
        'empty': False
    },
    'service_name': {
        'type': 'string',
        'required': False,
        'empty': False
    },
    'upstream': {
        'type': 'string',
        'required': False,
        'empty': False
    }
}


def validate_proxy(proxy):
    validator = Validator(_PROXY_SCHEMA, allow_unknown=False)

    try:
        document_state = validator.validate(proxy)
    except DocumentError:
        raise exc.ValidationError('Validation failed due Document Error')

    if not document_state:
        raise exc.ValidationError('Validation Failed', errors=validator.errors)
    return validator.document


def validate_service(service):
    validator = Validator(_SERVICES_SCHEMA, allow_unknown=False)

    try:
        document_state = validator.validate(service)
    except DocumentError:
        raise exc.ValidationError('Validation failed due Document Error')
    if not document_state:
        raise exc.ValidationError('Validation Failed', errors=validator.errors)

    return validator.document
