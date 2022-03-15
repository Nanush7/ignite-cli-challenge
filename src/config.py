"""
CLI config.
"""
from os.path import join
from pathlib import Path

CLI_ROOT_DIR = Path(__file__).parent.parent

PROMETEO_SANDBOX_URL = 'https://test.prometeo.qualia.uy/'

API_KEY_PATH = join(CLI_ROOT_DIR, '.api_key')
