from os.path import exists
from typing import List

import src.config as config
from src.client import ExtendedBankingClient, PrometeoClient
from src.exceptions import MissingAPIKey
from src.plugins import BasePlugin
from src.utils import Utils


class CLI:
    """
    CLI Class.
    """
    def __init__(self, out, api_key: str = ''):
        self.out = out
        self.api_key = api_key
        self.environment = config.DEFAULT_ENVIRONMENT
        self.env_list = [
            key for key in ExtendedBankingClient.ENVIRONMENTS.keys()]
        self.plugins = []

        # TODO: se van.
        self.client = None
        self.utils = Utils()

    def banner(self):
        banner_art = '''
     ____                           _                ____ _     ___ 
    |  _ \ _ __ ___  _ __ ___   ___| |_ ___  ___    / ___| |   |_ _|
    | |_) | '__/ _ \| '_ ` _ \ / _ \ __/ _ \/ _ \  | |   | |    | | 
    |  __/| | | (_) | | | | | |  __/ ||  __/ (_) | | |___| |___ | | 
    |_|   |_|  \___/|_| |_| |_|\___|\__\___|\___/   \____|_____|___|
    '''
        self.out.clear()
        self.out.red(banner_art)

    def get_api_key(self, request_change: bool = False) -> str:
        """
        Si se está utilizando por primera vez,
        pedirle al usuario el api key de Prometeo, el cual
        se puede guardar en .api_key
        """
        if not exists(config.API_KEY_PATH) or request_change:

            print(f'Please, enter you api key.')
            print('You may provide your key using the -k argument instead (Not recommended).')
            api_key = input('Your API key (leave blank to cancel): ')

            if not api_key:
                raise MissingAPIKey

            # Por defecto es 'no', por razones de seguridad.
            save = self.utils.query_yes_no(f'Save API key? (it will be saved in {config.API_KEY_PATH})', 'no')

            if save:
                with open(config.API_KEY_PATH, 'w') as file:
                    file.write(api_key.strip())

        else:
            with open(config.API_KEY_PATH, 'r') as file:
                api_key = file.readline()

        return api_key

    def get_plugins(self) -> List[BasePlugin]:
        """
        Get list of plugins.
        """
        plugins = []
        for plugin in BasePlugin.plugin_list:
            try:
                instance = plugin(self.client, self.out)
                self.out.success(f'<{plugin.name}> loaded.')
            except Exception:
                self.out.warning(f'Could not import <{plugin.name}> plugin.')
            else:
                plugins.append(instance)

        return plugins

    def set_env(self) -> None:
        """
        Change Prometeo environment.
        """
        # Print options.
        print('Change environment to:')
        for index, env in enumerate(self.env_list):
            print(f'[{index+1}] {env}.')

        # Ask for an option and change environment.
        option = int(input('--> '))
        if option < 1:
            raise ValueError

        self.environment = self.client.environment = self.env_list[option-1]

    def print_invalid_option(self) -> None:
        """
        Simplemente muestra el mensaje de
        opción inválida.
        """
        self.out.yellow('You had one job...')

    def menu(self):
        # Print banner.
        self.banner()

        # Mostrar opciones.
        self.out.blue('''
Options:
    => 'd' to get a description of all the plugins available.
    => 'c' to change the current environment.
    => 'k' to change your api_key.
    => 'quit' to exit.
        ''')

        # Mostrar environment activo.
        for env in self.env_list:
            if env != self.environment:
                print(f'   · {env}')
            else:
                self.out.green(f'   => {env}')

        print('')

        # Mostrar estado de la session.
        print('  Status => ', end='')
        status = self.client.status
        if status == config.LOGGED_OUT_STATUS:
            self.out.red('Logged out')
        elif status == config.LOGGED_IN_STATUS:
            self.out.green('Logged in')
        elif status == config.PROMETEO_ERROR_STATUS:
            self.out.red('Prometeo error')
        else:
            self.out.red(status)

        print('')

        # Mostrar plugins.
        for index, plugin in enumerate(self.plugins):
            self.out.yellow(f' >> {[index + 1]} {plugin.name}')

        if len(self.plugins) == 0:
            self.out.yellow('0 plugins loaded')

        # Pedir elección al usuario hasta
        # que proporcione una opción correcta.
        while True:
            choice = input('\n--> ').lower()

            # Opciones #
            # Terminar ejecución.
            if choice in ('exit', 'quit'):
                # TODO: Cerrar sesión.
                print('Quitting...')
                exit(0)

            # Mostrar descripciones para los plugins cargados.
            elif choice == 'd':
                for plugin in self.plugins:
                    print(f'{plugin.name}: {plugin.description}')

            # Cambiar de environment
            elif choice == 'c':
                self.set_env()

            # Cambiar api key.
            elif choice == 'k':
                try:
                    self.api_key = self.client.api_key = self.get_api_key(True)
                except MissingAPIKey:
                    pass

            # Ejecutar plugin.
            else:
                try:
                    index = int(choice) - 1
                    if index < 0:
                        raise IndexError

                    # Ejecutar la opción de la lista de plugins.
                    # Los plugins manipulan el objeto client (sí, suena feo).
                    # Le agregar o modifican datos.
                    self.plugins[index].run(self.client)

                except (IndexError, ValueError):
                    self.print_invalid_option()
                    continue

            # Volver al menú.
            break

    def run(self):
        # Pedir api_key al usuario
        # y obtener el cliente de Prometeo.
        self.out.info('Creating Prometeo client.')
        if not self.api_key:
            # (si no se agregó -k)
            self.api_key = self.get_api_key()
        self.client = PrometeoClient(self.api_key, self.environment)
        self.out.success(f'Created API client with {self.environment} scope.')

        # Obtener plugins.
        self.out.info('Loading plugins.')
        self.plugins = self.get_plugins()

        while True:
            # Pausar para que el usuario vea los resultados
            # antes de limpiar la pantalla de la consola.
            input('\nPress enter to continue...')
            self.menu()
