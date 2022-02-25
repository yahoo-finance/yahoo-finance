import datetime
import sys
from pprint import pprint

from yahoo_finance import Share

yahoo = Share('YHOO')

pprint (yahoo.get_historical('2014-04-25', '2014-04-29'))

