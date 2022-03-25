from prometeo import Client
from prometeo.banking.client import BankingAPIClient


SANDBOX_URL = 'https://banking.sandbox.prometeoapi.com/'
TESTING_URL = 'https://test.prometeo.qualia.uy'
PRODUCTION_URL = 'https://prometeo.qualia.uy'


class ExtendedBankingClient(BankingAPIClient):
    ENVIRONMENTS = {
            'sandbox': SANDBOX_URL,
            'testing': TESTING_URL,
            'production': PRODUCTION_URL
        }


class PrometeoClient(Client):
    def __init__(self, api_key: str, environment: str = 'sandbox'):
        self._api_key = api_key
        self._environment = environment
        self._banking = None
        self._session = None
        super().__init__(api_key, environment)

    @property
    def banking(self):
        if self._banking is None:
            self._banking = ExtendedBankingClient(
                self._api_key, self._environment
        )
        return self._banking

    def login(self, provider, username, password, **kwargs):
        self._session = self._banking.login(provider, username, password, **kwargs)
        return self._session
