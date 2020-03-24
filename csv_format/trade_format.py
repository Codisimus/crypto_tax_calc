from decimal import Decimal

from csv_format.csv_format import CSVFormat

two_places = Decimal(10) ** -2


class TradeFormat(CSVFormat):
    def to_string_array(self, trade):
        return [
            trade.size,
            trade.product,
            trade.date_acquired.strftime(self.date_format),
            trade.cost_basis.quantize(two_places),
            trade.date_sold.strftime(self.date_format),
            trade.fee.quantize(two_places),
            trade.proceeds.quantize(two_places),
            trade.gain.quantize(two_places)
        ]
