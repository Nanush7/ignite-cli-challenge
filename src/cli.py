from os.path import exists
from typing import List

import src.config as config
from src.client import ExtendedBankingClient, PrometeoClient
from src.exceptions import MissingAPIKey
from src.plugins import BasePlugin
from src.utils import Utils


class CLI:
    """
    CLI main interface.
    """
    def __init__(self, out, api_key: str = ''):
        self.api_key = api_key
        self.environment = config.DEFAULT_ENVIRONMENT
        self.env_list = [
            key for key in ExtendedBankingClient.ENVIRONMENTS.keys()]
        self.plugins = []

        self.out = out
        self.client = None
        self.utils = Utils(self.out)

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
            api_key = self.utils.get_option(type='str', required=False, input_prefix='Your API key (leave blank to cancel): ')

            if api_key is None:
                # Si era para cambiar, solo volver al menú.
                if request_change:
                    return
                # Si no había api_key, da error.
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
                self.out.success(f'<{plugin.plugin_name}> loaded.')
            except Exception:
                self.out.warning(f'Could not import <{plugin.plugin_name}> plugin.')
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
        option = self.utils.get_option()
        if option < 1 or option > len(self.env_list):
            self.out.yellow('Invalid option.')
            return

        self.environment = self.client.environment = self.env_list[option-1]

    def menu(self):
        # Mostrar banner (antes limpia la pantalla).
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
            self.out.yellow(f' >> {[index + 1]} {plugin.plugin_name}')

        if len(self.plugins) == 0:
            self.out.yellow('0 plugins loaded')

        print('')

        # Pedir elección al usuario.
        choice = self.utils.get_option(type='str').lower()

        # Opciones #
        # Terminar ejecución.
        if choice in ('exit', 'quit', 'e', 'q'):
            self.out.info('Closing plugins...')
            for plugin in self.plugins:
                try:
                    plugin.close()
                    self.out.success(f'<{plugin.plugin_name}> closed successfully.')
                except Exception:
                    self.out.warning(f'<{plugin.plugin_name}> did not close properly.')

            print('\nSee you! :)\n')
            exit(0)

        # Mostrar descripciones para los plugins cargados.
        elif choice == 'd':
            for plugin in self.plugins:
                print(f'{plugin.plugin_name}: {plugin.plugin_description}\n')

        # Cambiar de environment
        elif choice == 'c':
            self.set_env()

        # Cambiar api key.
        elif choice == 'k':
            self.api_key = self.client.api_key = self.get_api_key(request_change=True)

        # Si no es ninguna de las opciones anteriores,
        # intentar ejecutar un plugin de la lista.
        else:
            try:
                index = int(choice) - 1

                if index < 0 or index > len(self.plugins) - 1:
                    raise IndexError

            except (IndexError, ValueError):
                self.out.yellow('Invalid option.')
                return

            # Ejecutar la opción de la lista de plugins.
            # Los plugins manipulan el objeto client (sí, suena feo).
            # Le agregar o modifican datos.
            # Esto se deja fuera del try para evitar
            # tomar los IndexError y ValueError de los plugins.
            self.plugins[index].run()

    def run(self):
        # Pedir api_key al usuario
        # y obtener el cliente de Prometeo.
        self.out.info('Creating Prometeo client...')
        if not self.api_key:
            # (si no se agregó -k)
            self.api_key = self.get_api_key()
        self.client = PrometeoClient(self.api_key, self.environment)
        self.out.success(f'Created API client with {self.environment} scope.')

        # Obtener plugins.
        self.out.info('Loading plugins...')
        self.plugins = self.get_plugins()

        while True:
            # Pausar para que el usuario vea los resultados
            # antes de limpiar la pantalla de la consola.
            input('\nPress enter to continue...')
            self.menu()
