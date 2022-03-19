import src.plugins as plugins

class LoginPlugin(plugins.BasePlugin):
    name = 'Login'
    description = 'Get credentials and do login.'

    def run(self):
        print('Módulo ' + str(__file__) + ' cargado.')
