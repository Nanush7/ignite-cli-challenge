from typing import List

from prometeo.banking.client import BankingAPIClient
from prometeo.banking.models import Account, Movement

from src.config import LOGGED_IN_STATUS, LOGGED_OUT_STATUS

SANDBOX_URL = 'https://banking.sandbox.prometeoapi.com/'
TESTING_URL = 'https://test.prometeo.qualia.uy'
PRODUCTION_URL = 'https://prometeo.qualia.uy'


class ExtendedBankingClient(BankingAPIClient):
    ENVIRONMENTS = {
        'sandbox': SANDBOX_URL,
        'testing': TESTING_URL,
        'production': PRODUCTION_URL
    }

    def get_provider_detail(self, provider_code):
        """
        Se sobreescribe este método para arreglar un problema
        de la librería de prometeo.
        """
        data = self.call_api('GET', '/provider/{}/'.format(provider_code))
        return data


class PrometeoClient:
    """
    Esta clase solo hace uso de BankingAPIClient,
    todo lo demás de la clase prometeo.Client se omite.

    Acerca del uso de properties:
    La idea es que cada vez que se modifica la API key
    o el environment, se cierre la sesión y se cambien
    los campos correspondientes en cliente de banking.
    """

    def __init__(self, api_key: str, environment: str):
        # Usados en los plugins:
        self._api_key = api_key
        self._environment = environment
        self.status = LOGGED_OUT_STATUS

        # Se manejan internamente:
        self._banking = self._get_banking_client()
        self._session = None

    @property
    def environment(self):
        return self._environment

    @environment.setter
    def environment(self, env):
        self.logout()
        self._environment = env
        self._banking._environment = env

    @property
    def api_key(self):
        return self._api_key

    @api_key.setter
    def api_key(self, api_key):
        self.logout()
        self._api_key = api_key
        self._banking._api_key = api_key

    def _get_banking_client(self) -> ExtendedBankingClient:
        banking = ExtendedBankingClient(
            self.api_key, self.environment
        )
        return banking

    def login(self, provider, username, password, **kwargs) -> None:
        self._session = self._banking.login(
            provider, username, password, **kwargs)

    def logout(self) -> bool:
        """
        Invalidate Prometeo session key.
        Returns True if logout was successful.
        """
        # No intentar logout si el usuario no hizo login primero.
        if self.status == LOGGED_IN_STATUS:
            self._banking.logout(self._session.get_session_key())
            self.status = LOGGED_OUT_STATUS
            self._session = None
            return True

        return False

    def get_providers(self) -> List[tuple]:
        return self._banking.get_providers()

    def get_bank_accounts(self) -> List[Account]:
        """
        'Wrapper' para que el usuario no tenga que pasarle
        la session key.
        """
        session_key = self.get_session_key()
        return self._banking.get_accounts(session_key)

    def get_credit_cards(self) -> List[Account]:
        """
        'Wrapper' para que el usuario no tenga que pasarle
        la session key.
        """
        session_key = self.get_session_key()
        return self._banking.get_credit_cards(session_key)

    def get_movements(self, account_number, currency_code, start, end) -> List[Movement]:
        session_key = self.get_session_key()
        return self._banking.get_movements(session_key, account_number, currency_code, start, end)

    def get_credit_card_movements(self, account_number, currency_code, start, end) -> List[Movement]:
        session_key = self.get_session_key()
        return self._banking.get_credit_card_movements(session_key, account_number, currency_code, start, end)

    def get_session_key(self) -> str:
        if self._session:
            return self._session._session_key
        return None
