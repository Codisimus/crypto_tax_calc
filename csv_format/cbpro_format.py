from csv_format.transaction_format import TransactionFormat


class CoinbaseProFormat(TransactionFormat):
    def __init__(self):
        columns = ['side', 'size', 'size unit', 'created at', 'fee', 'total']
        date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        super().__init__(columns, date_format)
