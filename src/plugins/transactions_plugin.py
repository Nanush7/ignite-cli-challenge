import src.plugins as plugins

class TransactionsPlugin(plugins.BasePlugin):
    name = 'Transactions'
    description = 'Get transactions info.'

    def run(self):
        print('Módulo ' + str(__file__) + ' cargado.')
