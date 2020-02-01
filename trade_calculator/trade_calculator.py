from operator import attrgetter
from transaction import Action, clone_transaction
from trade import Trade

class TradeCalculator:
  def __init__(self, transactions):
    self.transactions = sorted(transactions, key=attrgetter('date'), reverse=True)
    self.buys = []
    self.trades = []

  def get_next_transaction(self):
    return self.transactions.pop()

  def readd_transaction(self, transaction):
    self.transactions.append(transaction)

  def add_buy(self, transaction):
    raise Error()

  def get_buy(self):
    return self.buys.pop()

  def readd_buy(self, transaction):
    self.buys.append(transaction)

  def add_trade(self, buy, sell):
    self.trades.append(Trade(buy, sell))

  def process(self):
    while len(self.transactions) > 0:
      transaction = self.get_next_transaction()
      if transaction.action == Action.BUY:
        self.add_buy(transaction)
      else:
        sell = transaction
        buy = self.get_buy()
        if buy.size < sell.size:
          sell, extra = self.split(sell, buy.size)
          self.readd_transaction(extra)
        elif buy.size > sell.size:
          buy, extra = self.split(buy, sell.size)
          self.readd_buy(extra)
        self.add_trade(buy, sell)
    return self.trades

  def split(self, transaction, size):
    #Rounding errors are possible here but result is
    # still more precise than your typical currency
    cost_multiplier = transaction.total / transaction.size
    fee_multiplier = transaction.fee / transaction.size
    first_total = cost_multiplier * size
    first_fee = fee_multiplier * size
    remainder = transaction.size - size;
    second_total = cost_multiplier * remainder
    second_fee = fee_multiplier * remainder
    first = clone_transaction(transaction, size, first_fee, first_total)
    second = clone_transaction(transaction, remainder, second_fee, second_total)
    return first, second