import datetime

import src.plugins as plugins
from prometeo.banking.exceptions import BankingClientError
from src.config import LOGGED_IN_STATUS
from src.exceptions import ValidationError

# Cambiar según lo requerido.
AVAILABLE_CURRENCIES = ['UYU', 'USD']
DEFAULT_DAY_INTERVAL = 30
MIN_WARNING_INTERVAL = 31

class TransactionsPlugin(plugins.BasePlugin):
    plugin_name = 'Transactions'
    plugin_description = 'Bank and credit card movements plugin. (!) Requires a session.'

    def run(self):
        if self.client.status != LOGGED_IN_STATUS:
            self.out.error('You must have an active session. (Try using Sessions plugin).')
            return

        print("""
Options:

    [1] Bank accounts.
    [2] Credit Cards.
        """)
        option = self.utils.get_option(required=False)
        if option == 1:
            accounts = self.get_bank_accounts()
        elif option == 2:
            accounts = self.get_credit_cards()
        else:
            if option is not None:
                self.out.yellow('Invalid option, try again.')
            return

        # Pedir parámetros para los movimientos:

        # Número de cuenta.
        account_choice = self.utils.get_option(required=False, input_prefix='Select an account (blank to exit) -> ')
        if account_choice is None:
            return
        if account_choice > len(accounts):
            self.out.yellow('Invalid choice. Try again.')
            return

        account_selected = accounts[account_choice-1]
        account_number = account_selected.number

        # Moneda.
        print('Select a currency:')
        for index, currency in enumerate(AVAILABLE_CURRENCIES):
            print(f'[{index+1}] {currency}')

        currency_choice = self.utils.get_option(required=True)
        currency = AVAILABLE_CURRENCIES[currency_choice-1]

        # Fecha de inicio y fin.
        today = datetime.date.today()
        default_start = self._date_to_str(today - datetime.timedelta(days=DEFAULT_DAY_INTERVAL))
        default_end = self._date_to_str(today)

        start_date_str = self.utils.get_option(
            type='str',
            required=False,
            input_prefix=f'Start date [{default_start}]: ',
            extra_validation=self._date_validation
        ) or default_start

        end_date_str = self.utils.get_option(
            type='str',
            required=False,
            input_prefix=f'End date [{default_end}]: ',
            extra_validation=self._date_validation
        ) or default_end

        start_date = self._str_to_date(start_date_str)
        end_date = self._str_to_date(end_date_str)

        if start_date > end_date:
            self.out.error('Invalid date interval. Try again.')
            return

        # Revisar que el intervalo no sea muy grande para evitar
        # sobrecargar a Prometeo.
        day_diff = end_date - start_date
        if day_diff.days >= MIN_WARNING_INTERVAL:
            self.out.warning('You are requesting a broad time interval.')
            question = self.utils.query_yes_no('Continue?', None)
            if not question:
                return

        # Obtener movimientos desde Prometeo.
        self.out.info('Requesting movements to Prometeo...')
        try:
            if option == 1:  # Cuenta de banco.
                movements = self.client.get_movements(account_number, currency, start_date, end_date)
            elif option == 2:  # Tarjeta de crédito.
                movements = self.client.get_credit_card_movements(account_number, currency, start_date, end_date)

        except BankingClientError:
            self.out.error('No account found with the selected currency.')
            return

        # Mostrar movimientos.
        self._show_movements(movements, currency)

    def get_bank_accounts(self):
        # Get user accounts.
        self.out.info('Requesting accounts to Prometeo...')
        accounts = self.client.get_bank_accounts()
        for index, account in enumerate(accounts):
            print(f"""
--------------------------
[{index+1}]
* Name: {account.name}
* Id: {account.id}
* Number: {account.number}
* Currency: {account.currency}
* Balance: {account.balance}
--------------------------""")

        return accounts

    def get_credit_cards(self):
        # Get user accounts.
        self.out.info('Requesting credit cards to Prometeo...')
        accounts = self.client.get_credit_cards()
        for index, account in enumerate(accounts):
            print(f"""
--------------------------
[{index+1}]
* Name: {account.name}
* Id: {account.id}
* Number: {account.number}
* Close date: {self._date_to_str(account.close_date)}
* Due date: {self._date_to_str(account.due_date)}
* Balance local: {account.balance_local}
* Balance (USD): {account.balance_dollar}
--------------------------""")

        return accounts

    def _date_validation(self, date):
        """
        Intentar convertir a un objeto de fecha.
        """
        try:
            datetime.datetime.strptime(date, "%d/%m/%Y")
        except Exception:
            raise ValidationError

    def _date_to_str(self, date) -> str:
        """
        Date to string.
        """
        return datetime.datetime.strftime(date, "%d/%m/%Y")

    def _str_to_date(self, string):
        return datetime.datetime.strptime(string, "%d/%m/%Y")

    def _show_movements(self, movements, currency) -> None:
        for movement in movements:
            self.out.blue(f"""
--------------------------
{movement.id} - {movement.reference} - {self._date_to_str(movement.date)}
* Detail: {movement.detail}
* Debit: ${currency} {movement.debit or 0}
* Credit: ${currency} {movement.credit or 0}""")

        # Close.
        self.out.blue('--------------------------')
