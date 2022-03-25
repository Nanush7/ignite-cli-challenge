import src.plugins as plugins

class MetaPlugin(plugins.BasePlugin):
    name = 'Meta'
    description = 'Get Meta information.'

    def __init__(self, client):
        super().__init__(client)

    def run(self):
        print('Módulo ' + str(__file__) + ' cargado.')
