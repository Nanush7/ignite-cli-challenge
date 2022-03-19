import src.plugins as plugins

class MetaPlugin(plugins.BasePlugin):
    name = 'Meta'
    description = 'Get Meta information.'

    def run(self):
        print('Módulo ' + str(__file__) + ' cargado.')
