import src.plugins as plugins

class SessionPlugin(plugins.BasePlugin):
    name = 'Sessions'
    description = 'Basic login and logout plugin.'

    def __init__(self, client):
        super().__init__(client)

    #def run(self):
    #    print('Módulo ' + str(__file__) + ' cargado.')
