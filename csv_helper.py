import os
import csv
import configparser
from datetime import datetime
from transaction import Action, Transaction

date_format = '%Y-%m-%dT%H:%M:%S.%fZ'

trade_csv_format = ['size', 'product', 'date_acquired', 'cost_basis', \
                    'date_sold', 'fee', 'proceeds', 'gain']

csv_formats = {
  'cbpro_csv_format': ['side', 'size', 'size unit', 'created at', 'fee', 'total']
  }

config = configparser.RawConfigParser()
config.read('config.properties')
section = config['Transaction']

tax_year = int(section.get('tax_year'))
target_product = section.get('product')
fail_on_mismatch = section.getboolean('fail_on_mismatch')
csv_format = csv_formats[section.get('csv_format')]

def get_export_path(file_path):
  dir_path = 'export'
  if not os.path.exists(dir_path):
    os.makedirs(dir_path)
  return dir_path + '/' + file_path

def load_transactions(path):
  transactions = []
  with open(path, newline='') as file:
    for row in csv.DictReader(file):
      action = Action[row[csv_format[0]]]
      size = float(row[csv_format[1]])
      product = row[csv_format[2]]
      date = datetime.strptime(row[csv_format[3]], date_format)
      fee = float(row[csv_format[4]])
      total = float(row[csv_format[5]])
      transaction = Transaction(action, size, product, date, fee, total)
      if ((action == Action.BUY or date.year == tax_year)
          and product == target_product):
        transactions.append(transaction)
      elif fail_on_mismatch:
        raise Exception('Unwanted Transaction in CSV: ' + str(transaction))
  return transactions

def write_trades(trades, file_path):
  with open(get_export_path(file_path), 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=trade_csv_format)
    writer.writeheader()
    for trade in trades:
      writer.writerow(vars(trade))

def write_transactions(transactions, file_path):
  with open(get_export_path(file_path), 'w', newline='') as file:
    writer = csv.DictWriter(file, fieldnames=csv_format)
    writer.writeheader()
    for transaction in transactions:
      writer.writerow({
        csv_format[0]: transaction.action.name,
        csv_format[1]: transaction.size,
        csv_format[2]: transaction.product,
        csv_format[3]: transaction.date,
        csv_format[4]: transaction.fee,
        csv_format[5]: transaction.total
        })

def create_report(file_path):
  with open(file_path, 'w', newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='|')
    writer.writerow([
      'type',
      'short_term_trades',
      'long_term_trades',
      'total_trades',
      'remaining_buys',
      'short_term_income',
      'long_term_income',
      'total_income',
      'tax_due'
      ])

def write_to_report(trade_calculator, file_path):
  short_term_trades = 0
  long_term_trades = 0
  short_term_income = 0
  long_term_income = 0
  for trade in trade_calculator.trades:
    date = trade.date_acquired
    date = date.replace(year = date.year + 1)
    if date > trade.date_sold:
      short_term_trades += 1
      short_term_income += trade.gain
    else:
      long_term_trades += 1
      long_term_income += trade.gain
  total_trades = short_term_trades + long_term_trades
  total_income = short_term_income + long_term_income
  with open(file_path, 'a', newline='') as file:
    writer = csv.writer(file, delimiter=',', quotechar='|')
    writer.writerow([
      trade_calculator.type,
      short_term_trades,
      long_term_trades,
      total_trades,
      len(trade_calculator.buys),
      round(short_term_income, 2),
      round(long_term_income, 2),
      round(total_income, 2),
      round(short_term_income * 0.1, 2)
      ])