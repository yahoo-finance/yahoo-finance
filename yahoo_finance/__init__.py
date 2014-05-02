import yql

from datetime import datetime
import pytz

__author__ = 'Lukasz Banasiak'
__version__ = '0.5.0'


def edt_to_utc(date, mask='%d/%m/%Y %I:%M%p'):
    utc = pytz.utc
    eastern = pytz.timezone('US/Eastern')
    date_ = datetime.strptime(date, mask)
    date_eastern = eastern.localize(date_, is_dst=None)
    date_utc = date_eastern.astimezone(utc)
    return date_utc


class YQLQueryError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Query failed with error: "%s".' % repr(self.value)


class YQLResponseMalformedError(Exception):

    def __str__(self):
        return 'Response malformed.'


class Currency(object):

    def __init__(self, symbol):
        self.symbol = symbol
        self.rate = self._fetch()

    @staticmethod
    def __request(symbol):
        response = yql.YQLQuery().execute('select * from yahoo.finance.xchange where pair in ("%s")' % symbol)
        try:
            return response['query']['results']
        except KeyError:
            try:
                raise YQLQueryError(response['error']['description'])
            except KeyError:
                raise YQLResponseMalformedError()

    def _fetch(self):
        data = self.__request(self.symbol)['rate']
        data['Datetime'] = edt_to_utc('%s %s' % (data['Date'], data['Time'])).strftime('%Y-%m-%d %H:%M:%S %Z%z')
        del data['Date'], data['Time']
        return data

    def refresh(self):
        self.rate = self._fetch()

    def get_bid(self):
        print self.rate['Bid']

    def get_ask(self):
        print self.rate['Ask']

    def get_rate(self):
        print self.rate['Rate']


class Share(object):
    pass


