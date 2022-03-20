from prometeo import Client
from prometeo.banking.client import BankingAPIClient


SANDBOX_URL = 'https://banking.sandbox.prometeoapi.com/'

class ExtendedBankingClient(BankingAPIClient):
    super.ENVIRONMENTS.update({'sandbox': SANDBOX_URL})

class PrometeoClient(Client):
    def __init__(self, api_key: str, environment: str = 'sandbox'):
        self.__api_key = api_key
        self.__environment = environment
        self.__banking = None

    @property
    def banking(self):
        if self.__banking is None:
            self.__banking = ExtendedBankingClient(
                self.__api_key, self.__environment
        )
