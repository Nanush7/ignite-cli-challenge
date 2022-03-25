import src.plugins as plugins

class TransactionsPlugin(plugins.BasePlugin):
    name = 'Transactions'
    description = 'Get transactions info.'

    def __init__(self, client):
        super().__init__(client)

    def run(self):
        print('Módulo ' + str(__file__) + ' cargado.')
