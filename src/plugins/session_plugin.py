import src.plugins as plugins
from prometeo import exceptions as prometeo_exc
from src.config import (LOGGED_IN_STATUS, LOGGED_OUT_STATUS,
                        PROMETEO_ERROR_STATUS, SANDBOX_CREDENTIALS,
                        WRONG_CREDENTIALS_STATUS)

from requests.exceptions import ConnectionError as RequestsConnError


class SessionPlugin(plugins.BasePlugin):
    plugin_name = 'Sessions'
    plugin_description = 'Basic login and logout plugin.'

    def run(self):
        self.out.blue("""
    >> [1] Login.
    >> [2] Logout.
        """)

        option = self.utils.get_option(required=False)
        try:
            if option == 1:
                self._login()
            elif option == 2:
                self._logout()
            else:
                return

        except prometeo_exc.UnauthorizedError:
            self.out.error(
                'Invalid API key. Are you in the correct environment?')

        except (prometeo_exc.WrongCredentialsError, KeyError):
            # KeyError es por un error de la librería de Prometeo,
            # Que en algunos casos da KeyError al hacer el raise
            # de WrongCredentialsError.
            self.out.error('Wrong or missing credentials.')
            self.client.status = WRONG_CREDENTIALS_STATUS

        except prometeo_exc.PrometeoError:
            # Esto toma todas las demás exceptions
            # de Prometeo.
            self.out.error('Internal Prometeo error.')
            self.client.status = PROMETEO_ERROR_STATUS

        except RequestsConnError:
            self.out.error('No internet connection.')

    def close(self):
        # Hacer logout directo (omitir lo de self._logout).
        self.client.logout()

    def _login(self) -> None:

        if self.client.status == LOGGED_IN_STATUS:
            self.out.warning('Already logged in.')
            login_again = self.utils.query_yes_no(
                'Do you want to logout and login again?', 'no')
            if not login_again:
                return
            self._logout()

        if self.client.environment == 'sandbox':
            provider = SANDBOX_CREDENTIALS['provider']
            username = SANDBOX_CREDENTIALS['username']
            password = SANDBOX_CREDENTIALS['password']
        else:
            provider = self.utils.get_option('str', input_prefix='provider: ')
            username = self.utils.get_option('str', input_prefix='username: ')
            password = self.utils.get_password()

        # Este login guarda la session en el objeto client.
        self.client.login(provider, username, password)
        self.client.status = LOGGED_IN_STATUS
        self.out.success('Login successful')

    def _logout(self) -> None:
        logged_out = self.client.logout()
        self.client.status = LOGGED_OUT_STATUS

        if logged_out:
            self.out.success('Logout successful')
        else:
            self.out.error('Not logged in.')
