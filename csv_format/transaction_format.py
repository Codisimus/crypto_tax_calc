from datetime import datetime
from decimal import Decimal

import config_helper as config
from csv_format.csv_format import CSVFormat
from transaction import Action, Transaction

section = config.get_section('Transaction')
tax_year = int(section.get('tax_year'))
target_product = section.get('product')
fail_on_mismatch = section.getboolean('fail_on_mismatch')


class TransactionFormat(CSVFormat):
    def load(self, path):
        transactions = []
        for transaction in super().load(path):
            if ((transaction.action == Action.BUY or transaction.date.year == tax_year)
                    and transaction.product == target_product):
                transactions.append(transaction)
            elif fail_on_mismatch:
                raise Exception('Unwanted Transaction in CSV: ' + str(transaction))
        return transactions

    def from_string_array(self, values):
        action = Action[values[0]]
        size = Decimal(values[1])
        product = values[2]
        date = datetime.strptime(values[3], self.date_format)
        fee = Decimal(values[4])
        total = Decimal(values[5])
        return Transaction(action, size, product, date, fee, total)

    def to_string_array(self, transaction):
        return [
            transaction.action.name,
            transaction.size,
            transaction.product,
            transaction.date.strftime(self.date_format),
            transaction.fee,
            transaction.total
        ]
