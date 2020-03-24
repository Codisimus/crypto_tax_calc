from csv_format.trade_format import TradeFormat


class TurboTaxFormat(TradeFormat):
    def __init__(self):
        columns = ['Amount', 'Currency Name', 'Purchase Date', 'Cost Basis', 'Date sold', 'Fee', 'Proceeds',
                   'Taxable Income']
        date_format = '%m/%d/%y'
        super().__init__(columns, date_format)
