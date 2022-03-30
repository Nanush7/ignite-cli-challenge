import src.plugins as plugins
from prometeo.exceptions import UnauthorizedError

class MetaPlugin(plugins.BasePlugin):
    plugin_name = 'Meta'
    plugin_description = 'Get provider information.'

    def run(self):
        self.out.info('Requesting provider list...')
        try:
            providers = self.client.get_providers()
        except UnauthorizedError:
            self.out.error(
                'Invalid API key. Are you in the correct environment?')
            return

        # Ordenar por país.
        providers.sort(key=lambda e: e.country)

        search_pattern = self.utils.get_option(
            'str', False, 'Search pattern (leave blank to show all providers): ')

        print('')

        # Mostrar todo.
        if search_pattern is None:
            search_results = providers

        # Se busca alguna coincidencia en alguno de los campos
        # de cada provider.
        else:
            search_results = []
            for provider in providers:
                if search_pattern.strip().lower() in [field.lower() for field in provider]:
                    search_results.append(provider)

        # No hay resultados.
        if len(search_results) == 0:
            self.out.warning(f'Did not find a match for {search_pattern}.')
            return

        # Mostrar la lista de los resultados de búsqueda.
        for index, provider in enumerate(search_results):
            print(f'[{index+1}] {provider.name} ({provider.country})')

        # Mostrar detalles de la opción elegida.
        option = self.utils.get_option(
            required=False, input_prefix='(blank to exit, 0 to show all) --> ')
        if option is None:
            return
        if option > len(search_results):
            self.out.yellow('Invalid option.')
            return
        if option == 0:
            for provider in search_results:
                self._show_provider_info(provider.code)
        else:
            self._show_provider_info(search_results[option-1].code)

    def _show_provider_info(self, provider_code):
        """
        Obtener detalles del provider y mostrarlos.
        """
        provider = self.client._banking.get_provider_detail(provider_code)['provider']

        print(f"""
--------------------------
* Code: {provider['name']}
* Country: {provider['country']}
* Auth details:
        """)
        for field in provider['auth_fields']:
            print(f"""
    * Field: {field['name']}
    * Type: {field['type']}
    * Interactive: {str(field['interactive'])}
    * Optional: {str(field['optional'])}""")
        print('--------------------------')
