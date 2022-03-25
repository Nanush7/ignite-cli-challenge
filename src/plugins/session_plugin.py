import src.plugins as plugins

class SessionPlugin(plugins.BasePlugin):
    name = 'Sessions'
    description = 'Login and Logout'

    def __init__(self, client):
        super().__init__(client)

    def run(self):
        print('Módulo ' + str(__file__) + ' cargado.')
