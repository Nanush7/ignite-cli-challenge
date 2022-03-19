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

from src.cli import CLI
from src.output import Output


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
    connection.add_argument('-k', '--api-key', help='Your API key. NOT RECOMMENDED: this will save your key to your shell history file.', type=str, default='', dest='api_key')

    ### Parse arguments ###
    args = parser.parse_args()

    ### Run ###
    out = Output(args.no_colors)

    api_key = args.api_key

    cli = CLI(out, api_key)
    print('')
    cli.run()

if __name__ == '__main__':
    main()
