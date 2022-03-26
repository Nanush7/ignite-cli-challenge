"""
Plugin exception classes.
"""
class MissingMethod(Exception):
    """
    Se usa cuando falta implementar algún método
    requerido al crear una subclase de BasePlugin.
    """
    def __init__(self, missing_attribute):
        self.message = f'Missing {missing_attribute} attribute.'
