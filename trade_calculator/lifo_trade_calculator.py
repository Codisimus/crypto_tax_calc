from trade_calculator.trade_calculator import TradeCalculator


class LIFOTradeCalculator(TradeCalculator):
    def __init__(self, transaction):
        super().__init__(transaction)
        self.type = 'LIFO'

    def add_buy(self, transaction):
        self.buys.append(transaction)
