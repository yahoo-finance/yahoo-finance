#
#	and some forex
#
import datetime
import sys

from yahoo_finance import Currency

eur_pln = Currency('USDEUR')

print eur_pln.get_bid()

print eur_pln.get_ask()

print eur_pln.get_rate()

print eur_pln.get_trade_datetime()