import os

from colorama import Fore, init


class Output:
    """
    Agregar prefijos y colores.
    """
    def __init__(self, color: bool = True):
        if color:
            init(autoreset=True)
            self.colors = {
                'red': Fore.LIGHTRED_EX,
                'green': Fore.GREEN,
                'yellow': Fore.YELLOW,
                'blue': Fore.BLUE
            }
        else:
            self.colors = {
                'red': '',
                'green': '',
                'yellow': '',
                'blue': ''
            }
        self.colors.update({'reset': Fore.RESET})

    # Log messages.

    def info(self, msg: str) -> None:
        print('INFO => ' + msg)

    def success(self, msg: str) -> None:
        print(self.colors['green'] + 'OK => ' + self.colors['reset'] + msg)

    def warning(self, msg: str) -> None:
        print(self.colors['yellow'] + 'WARNING => ' + self.colors['reset'] + msg)

    def error(self, msg: str) -> None:
        print(self.colors['red'] + 'ERROR => ' + self.colors['reset'] + msg)

    # Just colored output.
    def red(self, msg: str) -> None:
        print(self.colors['red'] + msg)

    def yellow(self, msg: str) -> None:
        print(self.colors['yellow'] + msg)

    def blue(self, msg: str) -> None:
        print(self.colors['blue'] + msg)

    def green(self, msg: str) -> None:
        print(self.colors['green'] + msg)

    def clear(self) -> None:
        """
        Clear console screen.
        """
        if os.name == 'nt':
            os.system('cls')
        else:
            os.system('clear')
