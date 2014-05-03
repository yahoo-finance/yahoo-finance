import yql

from datetime import datetime
import pytz

__author__ = 'Lukasz Banasiak'
__version__ = '1.0.0'


def edt_to_utc(date, mask='%d/%m/%Y %I:%M%p'):
    """
    Convert EDT (Eastern Daylight Time) to UTC

    :param date: EDT date string e.g. '5/2/2014 4:00pm'
    :param mask: format of input date e.g '%d/%m/%Y %I:%M%'
    :return: UTC date string e.g '2014-03-05 12:23:00 UTC+0000'
    """
    utc = pytz.utc
    eastern = pytz.timezone('US/Eastern')
    date_ = datetime.strptime(date, mask)
    date_eastern = eastern.localize(date_, is_dst=None)
    date_utc = date_eastern.astimezone(utc)
    return date_utc.strftime('%Y-%m-%d %H:%M:%S %Z%z')


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
        self.data_set = self._fetch()

    @staticmethod
    def __request(symbol):
        response = yql.YQLQuery().execute('select * from yahoo.finance.xchange where pair = "{0}"'.format(symbol))
        try:
            return response['query']['results']
        except KeyError:
            try:
                raise YQLQueryError(response['error']['description'])
            except KeyError:
                raise YQLResponseMalformedError()

    def _fetch(self):
        data = self.__request(self.symbol)['rate']
        data[u'DateTimeUTC'] = edt_to_utc('%s %s' % (data['Date'], data['Time']))
        return data

    def refresh(self):
        """
        Refresh stock data

        """
        self.data_set = self._fetch()

    def get_bid(self):
        return self.data_set['Bid']

    def get_ask(self):
        return self.data_set['Ask']

    def get_rate(self):
        return self.data_set['Rate']

    def get_trade_datetime(self):
        return self.data_set['DateTimeUTC']


class Share(object):

    def __init__(self, symbol):
        self.symbol = symbol
        self.data_set = self._fetch()

    @staticmethod
    def __request(symbol):
        response = yql.YQLQuery().execute('select * from yahoo.finance.quotes where symbol = "{0}"'.format(symbol))
        try:
            return response['query']['results']
        except KeyError:
            try:
                raise YQLQueryError(response['error']['description'])
            except KeyError:
                raise YQLResponseMalformedError()

    @staticmethod
    def __request_historical(symbol, start_date, end_date):
        response = yql.YQLQuery().execute(
            'select * from yahoo.finance.historicaldata where symbol = "{0}" '
            'and startDate = "{1}" and endDate = "{2}"'.format(symbol, start_date, end_date)
        )
        try:
            return response['query']['results']
        except KeyError:
            try:
                raise YQLQueryError(response['error']['description'])
            except KeyError:
                raise YQLResponseMalformedError()

    @staticmethod
    def __request_information(symbol):
        response = yql.YQLQuery().execute('select * from yahoo.finance.stocks where symbol = "{0}"'.format(symbol))
        try:
            return response['query']['results']
        except KeyError:
            try:
                raise YQLQueryError(response['error']['description'])
            except KeyError:
                raise YQLResponseMalformedError()

    def _fetch(self):
        data = self.__request(self.symbol)['quote']
        data[u'LastTradeDateTimeUTC'] = edt_to_utc('%s %s' % (data['LastTradeDate'], data['LastTradeTime']))
        return data

    def refresh(self):
        """
        Refresh stock data

        """
        self.data_set = self._fetch()

    def get_price(self):
        return self.data_set['LastTradePriceOnly']

    def get_change(self):
        return self.data_set['Change']

    def get_volume(self):
        return self.data_set['Volume']

    def get_prev_close(self):
        return self.data_set['PreviousClose']

    def get_open(self):
        return self.data_set['Open']

    def get_avg_daily_volume(self):
        return self.data_set['AverageDailyVolume']

    def get_stock_exchange(self):
        return self.data_set['StockExchange']

    def get_market_cap(self):
        return self.data_set['MarketCapitalization']

    def get_book_value(self):
        return self.data_set['BookValue']

    def get_ebitda(self):
        return self.data_set['EBITDA']

    def get_dividend_share(self):
        return self.data_set['DividendShare']

    def get_dividend_yield(self):
        return self.data_set['DividendYield']

    def get_earnings_share(self):
        return self.data_set['EarningsShare']

    def get_days_high(self):
        return self.data_set['DaysHigh']

    def get_days_low(self):
        return self.data_set['DaysLow']

    def get_year_high(self):
        return self.data_set['YearHigh']

    def get_year_low(self):
        return self.data_set['YearLow']

    def get_50day_moving_avg(self):
        return self.data_set['FiftydayMovingAverage']

    def get_200day_moving_avg(self):
        return self.data_set['TwoHundreddayMovingAverage']

    def get_price_earnings_ratio(self):
        return self.data_set['PERatio']

    def get_price_earnings_growth_ratio(self):
        return self.data_set['PEGRatio']

    def get_price_sales(self):
        return self.data_set['PriceSales']

    def get_price_book(self):
        return self.data_set['PriceBook']

    def get_short_ratio(self):
        return self.data_set['ShortRatio']

    def get_trade_datetime(self):
        return self.data_set['LastTradeDateTimeUTC']

    def get_historical(self, start_date, end_date):
        """
        Get Yahoo Finance Stock historical prices

        :param start_date: string date in format '2009-09-11'
        :param end_date: string date in format '2009-09-11'
        :return: dict
        """
        return self.__request_historical(self.symbol, start_date, end_date)['quote']

    def get_info(self):
        """
        Get Yahoo Finance Stock Summary Information

        :return: dict
        """
        return self.__request_information(self.symbol)['stock']