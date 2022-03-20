
class MissingAPIKey(Exception):
    def __init__(self, message: str = 'API key not provided') -> None:
        self.message = message
