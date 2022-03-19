from os.path import exists
from typing import Dict

from src.config import API_KEY_PATH
from src.plugins import BasePlugin


class CLI:
    """
    CLI Class.
    """
    def __init__(self, out, api_key: str = None):
        self.out = out
        self.api_key = api_key
        self.plugins = []

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


    def get_api_key(request_change: bool = False) -> str:
        """
        Si se está utilizando por primera vez,
        pedirle al usuario el api key de Prometeo, el cual
        se guardará en .api_key
        """
        if not exists(API_KEY_PATH) or request_change:

            print(f'Please, enter you api key (it will be saved in {API_KEY_PATH}).')
            print('You may provide your key using the -k argument instead (Not recommended).')
            api_key = input('Your API key (leave blank to cancel): ')

            if not api_key:
                return None

            with open(API_KEY_PATH, 'w') as file:
                file.write(api_key)

        else:
            with open(API_KEY_PATH, 'r') as file:
                api_key = file.readline()

        return api_key

    def get_plugins(self) -> Dict[str, BasePlugin]:
        """
        Get list of plugins.
        """
        plugins = []
        for plugin in BasePlugin.plugin_list:
            try:
                instance = plugin()
                self.out.success(f'"{plugin.name}" loaded.')
            except Exception:
                self.out.warning(f'Could not import "{plugin.name}" plugin.')
            else:
                plugins.append(plugin)

        return plugins

    def menu(self):
        # Print banner.
        self.banner()

        # Mostrar opciones.
        self.out.blue('''
Options:
    => type 'd' to get a description of all the plugins available.
    => type 'exit' to exit.
        ''')
        for index, plugin in enumerate(self.plugins):
            self.out.yellow(f' {[index + 1]} {plugin.name}')

        # Pedir elección al usuario hasta
        # que proporcione una opción correcta.
        while True:
            choice = input('\n--> ').lower()

            # Terminar ejecución.
            if choice == 'exit' or choice == 'quit':
                print('Quitting...')
                exit(0)

            # Mostrar descripciones para los plugins cargados.
            elif choice == 'd':
                for plugin in self.plugins:
                    print(f'{plugin.name}: {plugin.description}')

            # Ejecutar opción.
            else:
                try:
                    index = int(choice) - 1
                    if index < 0:
                        raise IndexError
                    # Ejecutar la opción de la lista de plugins.
                    self.plugins[index]().run()
                    # Volver al menú.
                    break
                except (IndexError, ValueError):
                    # Validar que la opción sea un int >= 1.
                    self.out.yellow('Invalid option. Try again.')

    def run(self):
        self.out.info('Loading plugins.')
        self.plugins = self.get_plugins()
        while True:
            # Pausar para que el usuario vea los resultados
            # antes de limpiar la pantalla de la consola.
            input('\nPress enter to continue...')
            self.menu()
