"""
1. El CLI debe funcionar en Bash o en algún shell compatible con Bash (sh, ZSH, etc).

2. Se puede usar cualquier lenguaje de programación convencional y/o cualquier framework.

3. El scope del CLI debe incluir:

a. Authentication (login / logout).
b. Transactional data (accounts / credit cards).
c. Meta (providers).

4. El CLI debe ofrecer una manera de establecer un API Key propio.

5. Para desarrollar se debe usar el ambiente de Sandbox.

6. Se va a evaluar funcionalidad y creatividad.

7. La entrega debe ser en un repositorio de Git público.
"""
import argparse
from os.path import exists

import requests

from src.config import API_KEY_PATH
from src.output import Output


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


def main():

    ### Crear parser ###
    parser = argparse.ArgumentParser(description='PrometeoAPI CLI.')

    ### Crear grupos de argumentos ###
    required = parser.add_argument_group(title='Basic arguments')
    setup = parser.add_argument_group(title='Setup options')
    connection = parser.add_argument_group(title='Connection arguments')
    log_options = parser.add_argument_group(title='Log options')

    ### Crear argumentos ###
    log_options.add_argument('--no-color', help='Do not use colors for console output.', action='store_false', dest='no_colors')
    setup.add_argument('--change-key', help='Prompt to change the API key.', action='store_true', dest='change_api_key')
    connection.add_argument('-k', '--api-key', help='Your API key. NOT RECOMMENDED: this will save your key to your shell history.', type=str, default='', dest='api_key')

    ### Parse arguments ###
    args = parser.parse_args()

    ### Validar argumentos ###
    if args.change_api_key:
        args.api_key = get_api_key(request_change=True)

    ### Run ###
    out = Output(args.no_colors)

    api_key = args.api_key or get_api_key()

    # Terminar ejecución si no se recibe ninguna key.
    if not api_key:
        out.error('You must provide an API key.')
        exit(1)

    out.success(api_key)

if __name__ == '__main__':
    main()
