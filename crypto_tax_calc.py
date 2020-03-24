from decimal import Decimal, ROUND_HALF_UP

import config_helper as config
import csv_helper as io
from trade_calculator.fifo_trade_calculator import FIFOTradeCalculator
from trade_calculator.hafo_trade_calculator import HAFOTradeCalculator
from trade_calculator.hifo_trade_calculator import HIFOTradeCalculator
from trade_calculator.hpfo_trade_calculator import HPFOTradeCalculator
from trade_calculator.lafo_trade_calculator import LAFOTradeCalculator
from trade_calculator.lifo_trade_calculator import LIFOTradeCalculator
from trade_calculator.lofo_trade_calculator import LOFOTradeCalculator
from trade_calculator.lpfo_trade_calculator import LPFOTradeCalculator
from transaction import Action

section = config.get_section('Validation')
gross_transactions = Decimal(section.get('gross_transactions'))
number_transactions = int(section.get('number_transactions'))

report_file = 'report.csv'

two_places = Decimal(10) ** -2


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
    total_gross_transactions = Decimal(0)
    for trade in trade_calculator.trades:
        total_gross_transactions += trade.proceeds + trade.fee
    total_gross_transactions = total_gross_transactions.quantize(two_places, rounding=ROUND_HALF_UP)
    if total_gross_transactions != gross_transactions:
        warnings.append(str(total_gross_transactions) + ' gross transactions')
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


transactions = io.load_all_transactions()

io.create_report(report_file)

process(LIFOTradeCalculator(transactions))
process(FIFOTradeCalculator(transactions))
process(HPFOTradeCalculator(transactions))
process(LPFOTradeCalculator(transactions))
process(HIFOTradeCalculator(transactions))
process(LOFOTradeCalculator(transactions))
process(HAFOTradeCalculator(transactions))
process(LAFOTradeCalculator(transactions))
