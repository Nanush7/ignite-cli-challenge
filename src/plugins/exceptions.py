"""
Plugin exception classes.
"""
class MissingAttribute(Exception):
    """
    Se usa cuando falta algún atributo
    obglitario al crear una subclase de BasePlugin.
    """
    def __init__(self, missing_attribute):
        self.message = f'Missing {missing_attribute} attribute.'
