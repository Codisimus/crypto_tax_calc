from csv_format.transaction_format import TransactionFormat


class DefaultTransactionFormat(TransactionFormat):
    def __init__(self):
        columns = ['action', 'size', 'product', 'date', 'fee', 'total']
        date_format = '%Y-%m-%d %H:%M:%S.%f'
        super().__init__(columns, date_format)
