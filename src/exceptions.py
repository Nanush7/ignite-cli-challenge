
class MissingAPIKey(Exception):
    def __init__(self, message: str = 'API key not provided') -> None:
        self.message = message


class UnavailableType(Exception):
    def __init__(self, message: str = 'Type unavailable'):
        self.message = message


class ValidationError(Exception):
    def __init__(self, message: str = ''):
        self.message = message
