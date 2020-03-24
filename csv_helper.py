import csv
import os
from decimal import Decimal

import config_helper as config
from csv_format.cbpro_format import CoinbaseProFormat
from csv_format.default_trade_format import DefaultTradeFormat
from csv_format.default_transaction_format import DefaultTransactionFormat
from csv_format.turbo_tax_format import TurboTaxFormat

csv_formats = {
    'transaction': {
        'default': DefaultTransactionFormat(),
        'cbpro': CoinbaseProFormat()
    },
    'trade': {
        'default': DefaultTradeFormat(),
        'turbotax': TurboTaxFormat()
    }
}

trade_format = csv_formats['trade'][config.get('Export', 'format')]

section = config.get_section('Report')
short_term_tax_rate = Decimal(section.get('income_tax_rate'))
long_term_tax_rate = Decimal(section.get('long-term_capital_gains_tax_rate'))


def get_export_path(file_path):
    dir_path = 'export'
    if not os.path.exists(dir_path):
        os.makedirs(dir_path)
    return dir_path + '/' + file_path


def get_csv_format(name):
    return csv_formats['transaction'].get(name, csv_formats['transaction']['default'])


def load_all_transactions():
    transactions = []
    for filename in os.listdir('input'):
        if filename.endswith('.csv'):
            input_format = get_csv_format(filename[:-4])
            transactions.extend(input_format.load('input/' + filename))
    return transactions


def write_transactions(transactions, file_path):
    output_format = get_csv_format('default')
    output_format.write(transactions, get_export_path(file_path))


def write_trades(trades, file_path):
    trade_format.write(trades, get_export_path(file_path))


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
        date = date.replace(year=date.year + 1)
        if date > trade.date_sold:
            short_term_trades += 1
            short_term_income += trade.gain
        else:
            long_term_trades += 1
            long_term_income += trade.gain
    total_trades = short_term_trades + long_term_trades
    total_income = short_term_income + long_term_income
    tax_due = short_term_income * short_term_tax_rate + long_term_income * long_term_tax_rate
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
            round(tax_due, 2)
        ])
