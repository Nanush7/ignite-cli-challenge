import os
from importlib import util

from . import exceptions


class BasePlugin:
    """
    Base plugin class.
    """
    plugin_list = []
    name: str = None
    description: str = None

    def __init_subclass__(cls):
        """
        Añadir a plugins las clases que hereden de
        la clase BasePlugin y validar atributos y métodos
        obligatorios.
        """
        mandatory = {
            'name': cls.name,
            'description': cls.description,
            'run': cls.run
        }

        for key, value in mandatory.items():
            if not value:
                raise exceptions.MissingAttribute(key)

        cls.plugin_list.append(cls)

    def get_name(self) -> str:
        return self.name

    def run(self) -> None: ...

# Utilidad para cargar módulos automáticamente.
def load_module(path):
    name = os.path.split(path)[-1]
    spec = util.spec_from_file_location(name, path)
    module = util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


path = os.path.abspath(__file__)
dirpath = os.path.dirname(path)

for file_name in os.listdir(dirpath):
    if file_name.endswith('_plugin.py'):
        load_module(os.path.join(dirpath, file_name))
