from operator import attrgetter

from trade_calculator.trade_calculator import TradeCalculator


class HPFOTradeCalculator(TradeCalculator):
    def __init__(self, transaction):
        super().__init__(transaction)
        self.type = 'HPFO'

    def add_buy(self, transaction):
        self.buys.append(transaction)
        self.sort_buys()

    def sort_buys(self):
        self.buys.sort(key=attrgetter('price'))
