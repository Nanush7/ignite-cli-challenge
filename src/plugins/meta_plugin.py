import sqlite3
from src.config import CACHE_DB
import src.plugins as plugins

class MetaPlugin(plugins.BasePlugin):
    name = 'Meta'
    description = 'Get provider information.'

    def __init__(self, client, output):
        self.cache_conn = self._get_cache_db_conn()

        super().__init__(client, output)

    @staticmethod
    def sort_by_country():
        return

    def run(self):
        self.out.info('Requesting provider list...')
        # cache_response = self.utils.query_yes_no('Save provider list to cache?')
        # if cache_response:
        #     pass
        providers = self._client.get_providers()
        # Ordenar por país.
        providers.sort(key=lambda e : e.country)

        search_pattern = self.utils.get_option('str', False, 'Search pattern (leave blank to show all providers): ')

        if not search_pattern:
            search_results = providers
        else:
            search_results = []
            for provider in providers:
                for field in provider:
                    if search_pattern.strip().lower() in field.lower():
                        search_results.append(provider)                        

        if len(search_results) == 0:
            self.out.warning(f'Did not find a match for {search_pattern}.')
            return

        for index, provider in enumerate(search_results):
            print(f'[{index+1}] {provider.name} ({provider.country})')

        option = self.utils.get_option(required=False, input_prefix='(leave blank to exit) --> ')
        if not option:
            return

        provider_data = self._client._banking.get_provider_detail(search_results[option-1])  # TODO: Terminar.
        print(f"""
--------------------------
* Name: {provider_data.name}
* Country: {provider_data.country}
* Auth details: {provider_data.auth_details}
--------------------------
        """)

    def _get_cache_db_conn(self) -> sqlite3.Connection:
        conn = sqlite3.connect(CACHE_DB)
        return conn
