from prometeo.banking.client import BankingAPIClient

from src.config import LOGGED_OUT_STATUS

SANDBOX_URL = 'https://banking.sandbox.prometeoapi.com/'
TESTING_URL = 'https://test.prometeo.qualia.uy'
PRODUCTION_URL = 'https://prometeo.qualia.uy'


class ExtendedBankingClient(BankingAPIClient):
    ENVIRONMENTS = {
            'sandbox': SANDBOX_URL,
            'testing': TESTING_URL,
            'production': PRODUCTION_URL
        }


class PrometeoClient:
    """
    Esta clase solo hace uso de BankingAPIClient,
    todo lo demás de la clase prometeo.Client se omite.

    Acerca del uso de properties:
    La idea es que cada vez que se modifica la API key
    o el environment, se cierre la sesión y se cambien
    los campos correspondientes en cliente de banking.
    """
    def __init__(self, api_key: str, environment: str, **additional_data):
        # Usados en los plugins:
        self._api_key = api_key
        self._environment = environment
        self.status = LOGGED_OUT_STATUS
        self.data = additional_data

        # Se manejan internamente:
        self._banking = self._get_banking_client()
        self._session = None

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, env):
        self._environment = env
        self.logout()
        self._banking._environment = env

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        self._api_key = api_key
        self.logout()
        self._banking._api_key = api_key

    def _get_banking_client(self) -> ExtendedBankingClient:
        banking = ExtendedBankingClient(
            self.api_key, self.environment
        )
        return banking

    def login(self, provider, username, password, **kwargs) -> None:
        self._session = self._banking.login(provider, username, password, **kwargs)

    def logout(self) -> None:
        self._banking.logout(self._session.get_session_key())
        self._session = None
