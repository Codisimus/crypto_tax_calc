from enum import Enum

class Action(Enum):
  BUY = 1
  SELL = 2

class Transaction:
  def __init__(self, action, size, product, date, fee, total):
    self.action = action
    self.size = size
    self.product = product
    self.date = date
    self.fee = fee
    self.total = total
    self.__validate__()
    self.price = total / size

  def __validate__(self):
    if (self.size <= 0 or self.fee < 0
        or (self.action == Action.BUY and self.total >= 0)
        or (self.action == Action.SELL and self.total < 0)):
      raise Exception('Invalid Transaction: ' + self)

  def __str__(self):
    return str(self.action) + ' ' + str(self.size) + ' ' + self.product \
           + ' on ' + str(self.date) + ' for ' + str(self.total)

def clone_transaction(orig, size, fee, total):
  return Transaction(orig.action, size, orig.product, orig.date, fee, total)