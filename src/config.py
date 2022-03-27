"""
CLI config.
"""
from os.path import join
from pathlib import Path

CLI_ROOT_DIR = Path(__file__).parent.parent

API_KEY_PATH = join(CLI_ROOT_DIR, '.api_key')

# Utilizado por la clase utils.Utils
AVAILABLE_DATATYPES = ('int', 'float', 'str', 'chr')

DEFAULT_INPUT_PREFIX = '--> '

DEFAULT_ENVIRONMENT = 'sandbox'

PROMETEO_SANDBOX_URL = 'https://test.prometeo.qualia.uy/'

SANDBOX_CREDENTIALS = {
    'provider': 'test',
    'username': '12345',
    'password': 'gfdsa'
}

WRONG_CREDENTIALS_STATUS = 'wrong_credentials'
INTERACTION_STATUS = 'interaction_required'
LOGGED_IN_STATUS = 'logged_in'

# Esto no viene de Prometeo:
LOGGED_OUT_STATUS = 'logged_out'
PROMETEO_ERROR_STATUS = 'prometeo_error'

# TODO: Leer config de las clases de cada plugin.
