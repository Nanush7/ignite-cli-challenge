from colorama import init, Fore

class Output:
    """
    Print with message level prefix (colors are optional).
    """
    def __init__(self, color: bool = True):
        if color:
            init(autoreset=True)
            self.colors = {
                'red': Fore.LIGHTRED_EX,
                'green': Fore.GREEN,
                'yellow': Fore.YELLOW,
                'white': Fore.LIGHTWHITE_EX
            }
        else:
            self.colors = {
                'red': '',
                'green': '',
                'yellow': '',
                'white': ''
            }
        self.colors.update({'reset': Fore.RESET})

    def info(self, msg: str) -> None:
        print(self.colors['white'] + 'INFO::' + self.colors['reset'] + msg)

    def success(self, msg: str) -> None:
        print(self.colors['green'] + 'OK::' + self.colors['reset'] + msg)

    def warning(self, msg: str) -> None:
        print(self.colors['yellow'] + 'WARNING::' + self.colors['reset'] + msg)

    def error(self, msg: str) -> None:
        print(self.colors['red'] + 'ERROR::' + self.colors['reset'] + msg)