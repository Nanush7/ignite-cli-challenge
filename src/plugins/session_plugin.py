import src.plugins as plugins

class SessionPlugin(plugins.BasePlugin):
    name = 'Sessions'
    description = 'Login and Logout'

    def run(self):
        print('Módulo ' + str(__file__) + ' cargado.')
