import abc
import os
from importlib import util

import src.exceptions as exceptions
from src.client import PrometeoClient
from src.utils import Utils


class BasePlugin(metaclass=abc.ABCMeta):
    """
    Base plugin class.
    """
    plugin_list = []
    plugin_name: str = 'Unknown'  # Default.
    plugin_description: str = 'No description.'
    # Para usar en funciones de validación:
    ValidationError = exceptions.ValidationError

    def __init_subclass__(cls):
        """
        Añadir a plugins las clases que hereden de
        la clase BasePlugin.
        """
        cls.plugin_list.append(cls)

    def __init__(self, client, output):
        self._client = client  # TODO: sacar unserscore después de un commit.
        self.out = output
        self.utils = Utils(self.out)

    def close(self) -> None:
        """
        Este método será ejecutado al cerrar el cli.
        """
        pass

    @abc.abstractmethod
    def run(self, client: PrometeoClient) -> PrometeoClient:
        raise NotImplementedError


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
