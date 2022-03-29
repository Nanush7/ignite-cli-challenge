"""
MIT License

Copyright (c) 2020 Diego Moraes

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
"""

import sys
from getpass import GetPassWarning, getpass
from typing import Any

from src.config import AVAILABLE_DATATYPES, DEFAULT_INPUT_PREFIX


class UnavailableType(Exception):
    def __init__(self, message: str = 'Type unavailable'):
        self.message = message


class Utils:

    def __init__(self):
        pass

    def query_yes_no(self, question, default="yes"):
        """
        Author: Diego Moraes.

        Ask a yes/no question via raw_input() and return their answer.
        "question" is a string that is presented to the user.
        "default" is the presumed answer if the user just hits <Enter>.
            It must be "yes" (the default), "no" or None (meaning
            an answer is required of the user).
        The "answer" return value is True for "yes" or False for "no".
        """
        valid = {"yes": True, "y": True, "ye": True,
                "no": False, "n": False}
        if default is None:
            prompt = " [y/n] "
        elif default == "yes":
            prompt = " [Y/n] "
        elif default == "no":
            prompt = " [y/N] "
        else:
            raise ValueError("invalid default answer: '%s'" % default)

        while True:
            sys.stdout.write(question + prompt)
            choice = input().lower()
            if default is not None and choice == '':
                return valid[default]
            elif choice in valid:
                return valid[choice]
            else:
                sys.stdout.write("Please respond with 'yes' or 'no' "
                                "(or 'y' or 'n').\n")

    def get_option(self, type: str = 'int', required: bool = True, input_prefix: str = DEFAULT_INPUT_PREFIX) -> Any:
        """
        Author: Nanush7.

        Pedirle una entrada al usuario y validarla.
        """
        if type not in AVAILABLE_DATATYPES:
            raise UnavailableType(f'{type} not in AVAILABLE_DATATYPES.')

        option_type = eval(type)

        # Ejecutar hasta conseguir un input válido.
        while True:
            user_input = input(input_prefix)
            if user_input.strip() == '':
                if required:
                    self.out.yellow('Input required.')
                    continue
                else:
                    return None
            try:
                option = option_type(user_input)
            except TypeError:
                self.out.yellow('Invalid input.')
                continue

            return option

    def get_password(self, input_prefix: str = 'Password: ') -> str:
        try:
            password = getpass(input_prefix)
        except GetPassWarning:
            print('Unable to turn echo off for password input.')
            password = input(input_prefix)

        return password
