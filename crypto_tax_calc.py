import sys
sys.path.insert(0, 'trade_calculator/')
import locale
locale.setlocale(locale.LC_ALL, '')
import configparser
import csv_helper as io
from transaction import Action
from lifo_trade_calculator import LIFOTradeCalculator
from fifo_trade_calculator import FIFOTradeCalculator
from hpfo_trade_calculator import HPFOTradeCalculator
from lpfo_trade_calculator import LPFOTradeCalculator
from hifo_trade_calculator import HIFOTradeCalculator
from lofo_trade_calculator import LOFOTradeCalculator
from hafo_trade_calculator import HAFOTradeCalculator
from lafo_trade_calculator import LAFOTradeCalculator

config = configparser.RawConfigParser()
config.read('config.properties')
section = config['Validation']

gross_transactions = float(section.get('gross_transactions'))
number_transactions = int(section.get('number_transactions'))

report_file = 'report.csv'

def process(trade_calculator):
  trade_calculator.process()
  warnings = validate(trade_calculator)
  if len(warnings) > 0:
    print('WARNING - Validation failure for ' + trade_calculator.type)
    for warning in warnings:
      print('    ' + warning)
  export(trade_calculator)
  io.write_to_report(trade_calculator, report_file)

def validate(trade_calculator):
  warnings = []
  total_gross_transactions = 0
  for trade in trade_calculator.trades:
    total_gross_transactions += trade.proceeds + trade.fee
  if round(total_gross_transactions, 2) != gross_transactions:
    warnings.append(locale.currency(total_gross_transactions, grouping=True) \
                    + ' gross transactions')
  total_number_transactions = 0
  for transaction in transactions:
    if transaction.action == Action.SELL:
      total_number_transactions += 1
  if total_number_transactions < number_transactions:
    warnings.append(str(total_number_transactions) + ' transactions')
  return warnings

def export(trade_calculator):
  prefix = trade_calculator.type.lower() + '_'
  io.write_trades(trade_calculator.trades, prefix + 'trades.csv')
  io.write_transactions(trade_calculator.buys, prefix + 'remaining_buys.csv')


io.create_report(report_file)

transactions = io.load_transactions('transactions.csv')

process(LIFOTradeCalculator(transactions))
process(FIFOTradeCalculator(transactions))
process(HPFOTradeCalculator(transactions))
process(LPFOTradeCalculator(transactions))
process(HIFOTradeCalculator(transactions))
process(LOFOTradeCalculator(transactions))
process(HAFOTradeCalculator(transactions))
process(LAFOTradeCalculator(transactions))
