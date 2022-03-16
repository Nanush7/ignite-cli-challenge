from os.path import exists

from src.config import API_KEY_PATH


class CLI:
    """
    CLI Class.
    """
    def __init__(self, out, api_key: str = None):
        self.out = out
        self.api_key = api_key

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

    def menu(self):
        print('Options:')
        for index, option in enumerate(option_list):
            print(f'[{index + 1}] {option}')

    def run(self):
        self.banner()
