
class CoreException(Exception):
    def __init__(self, message):
        self.message = message


class ValidationError(CoreException):
    def __init__(self, message, errors=[]):
        super().__init__(message)
        self.errors = errors
