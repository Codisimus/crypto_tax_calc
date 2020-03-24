from csv_format.trade_format import TradeFormat


class DefaultTradeFormat(TradeFormat):
    def __init__(self):
        columns = ['size', 'product', 'date_acquired', 'cost_basis', 'date_sold', 'fee', 'proceeds', 'gain']
        date_format = '%Y-%m-%dT%H:%M:%S.%fZ'
        super().__init__(columns, date_format)
