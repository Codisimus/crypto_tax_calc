from trade_calculator.trade_calculator import TradeCalculator


class FIFOTradeCalculator(TradeCalculator):
    def __init__(self, transaction):
        super().__init__(transaction)
        self.type = 'FIFO'

    def add_buy(self, transaction):
        self.buys.insert(0, transaction)
