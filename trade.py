class Trade:
  def __init__(self, buy, sell):
    self.__validate__(buy, sell)
    self.size = buy.size
    self.product = buy.product
    self.date_acquired = buy.date
    self.cost_basis = -buy.total
    self.date_sold = sell.date
    self.fee = sell.fee
    self.proceeds = sell.total
    self.gain = self.proceeds - self.cost_basis

  def __validate__(self, buy, sell):
    if (buy.action == sell.action or buy.date > sell.date
       or buy.size != sell.size or buy.product != sell.product):
      raise Exception(buy + ' cannot be paired with ' + sell)

  def __str__(self):
    return str(self.size) + ' ' + self.product + ' (' + self.date_acquired \
           + '->' + self.date_sold + ') for ' + str(self.gain)