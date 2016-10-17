import yahoo_finance.yql

from datetime import datetime, timedelta
import pytz

__author__ = 'Lukasz Banasiak'
__version__ = '1.2.2'
__all__ = ['Currency', 'Share']


def edt_to_utc(date, mask='%m/%d/%Y %I:%M%p'):
    """
    Convert EDT (Eastern Daylight Time) to UTC

    :param date: EDT date string e.g. '5/26/2014 4:00pm'
    :param mask: format of input date e.g '%m/%d/%Y %I:%M%'
    :return: UTC date string e.g '2014-03-05 12:23:00 UTC+0000'
    """
    utc = pytz.utc
    eastern = pytz.timezone('US/Eastern')
    # date string for yahoo can contains 0 rather than 12.
    # This means that it cannot be parsed with %I see GH issue #15.
    date_ = datetime.strptime(date.replace(" 0:", " 12:"), mask)
    date_eastern = eastern.localize(date_, is_dst=None)
    date_utc = date_eastern.astimezone(utc)
    return date_utc.strftime('%Y-%m-%d %H:%M:%S %Z%z')


def get_date_range(start_day, end_day, step_days=365, mask='%Y-%m-%d'):
    """
    Split date range for a specified number of days.

    Generate tuples with intervals from given range of dates, e.g for `2012-04-25`-`2014-04-29`:

        ('2013-04-29', '2014-04-29')
        ('2012-04-28', '2013-04-28')
        ('2012-04-25', '2012-04-27')

    :param start_day: start date string
    :param end_day: end date string
    :param step_days: step days
    :param mask: format of input date e.g '%Y-%m-%d'
    """

    start = datetime.strptime(start_day, mask)
    end = datetime.strptime(end_day, mask)
    if start > end:
        raise ValueError('Start date "%s" is greater than "%s"' % (start_day, end_day))
    step = timedelta(days=step_days)
    while end - step > start:
        current = end - step
        yield current.strftime(mask), end.strftime(mask)
        end = current - timedelta(days=1)
    else:
        yield start.strftime(mask), end.strftime(mask)


class YQLQueryError(Exception):

    def __init__(self, value):
        self.value = value

    def __str__(self):
        return 'Query failed with error: "%s".' % repr(self.value)


class YQLResponseMalformedError(Exception):

    def __str__(self):
        return 'Response malformed.'


class Base(object):

    def __init__(self, symbol):
        self.symbol = symbol
        self._table = ''
        self._key = ''

    def _prepare_query(self, table='quotes', key='symbol', **kwargs):
        """
        Simple YQL query bulder

        """
        query = 'select * from yahoo.finance.{table} where {key} = "{symbol}"'.format(
            symbol=self.symbol, table=table, key=key)
        if kwargs:
            query += ''.join(' and {0}="{1}"'.format(k, v)
                             for k, v in kwargs.items())
        return query

    @staticmethod
    def _is_error_in_results(results):
        """
        Check if key name does not start from `Error*`

        For example when Symbol is not found we can find key:
        `"ErrorIndicationreturnedforsymbolchangedinvalid": "No such ticker symbol. (...)",`
        """
        # check if response is dictionary, skip if it is different e.g. list from `get_historical()`
        if isinstance(results, dict):
            return next((results[i] for i in results.keys() if 'Error' in i), False)

    @staticmethod
    def _change_incorrect_none(results):
        """
        Change N/A values to None

        """
        # check if response is dictionary, skip if it is different e.g. list from `get_historical()`
        if isinstance(results, dict):
            for k, v in results.items():
                if v:
                    if 'N/A' in v:
                        results[k] = None

    def _request(self, query):
        response = yql.YQLQuery().execute(query)
        try:
            _, results = response['query']['results'].popitem()
        except (KeyError, StopIteration, AttributeError):
            try:
                raise YQLQueryError(response['error']['description'])
            except KeyError:
                raise YQLResponseMalformedError()
        else:
            if self._is_error_in_results(results):
                raise YQLQueryError(self._is_error_in_results(results))
            self._change_incorrect_none(results)
            return results

    def _fetch(self):
        query = self._prepare_query(table=self._table, key=self._key)
        data = self._request(query)
        return data

    def refresh(self):
        """
        Refresh stock data

        """
        self.data_set = self._fetch()


class Currency(Base):

    def __init__(self, symbol):
        super(Currency, self).__init__(symbol)
        self._table = 'xchange'
        self._key = 'pair'
        self.refresh()

    def _fetch(self):
        data = super(Currency, self)._fetch()
        if data['Date'] and data['Time']:
            data[u'DateTimeUTC'] = edt_to_utc('{0} {1}'.format(data['Date'], data['Time']))
        return data

    def get_bid(self):
        return self.data_set['Bid']

    def get_ask(self):
        return self.data_set['Ask']

    def get_rate(self):
        return self.data_set['Rate']

    def get_trade_datetime(self):
        return self.data_set['DateTimeUTC']


class Share(Base):

    def __init__(self, symbol):
        super(Share, self).__init__(symbol)
        self._table = 'quotes'
        self._key = 'symbol'
        self.refresh()

    def _fetch(self):
        data = super(Share, self)._fetch()
        if data['LastTradeDate'] and data['LastTradeTime']:
            data[u'LastTradeDateTimeUTC'] = edt_to_utc('{0} {1}'.format(data['LastTradeDate'], data['LastTradeTime']))
        return data

    def get_price(self):
        return self.data_set['LastTradePriceOnly']

    def get_change(self):
        return self.data_set['Change']

    def get_percent_change(self):
        return self.data_set['PercentChange']

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

    def get_name(self):
        return self.data_set['Name']

    def get_historical(self, start_date, end_date):
        """
        Get Yahoo Finance Stock historical prices

        :param start_date: string date in format '2009-09-11'
        :param end_date: string date in format '2009-09-11'
        :return: list
        """
        hist = []
        for s, e in get_date_range(start_date, end_date):
            try:
                query = self._prepare_query(table='historicaldata', startDate=s, endDate=e)
                result = self._request(query)
                if isinstance(result, dict):
                    result = [result]
                hist.extend(result)
            except AttributeError:
                pass
        return hist

    def get_info(self):
        """
        Get Yahoo Finance Stock Summary Information

        :return: dict
        """
        query = self._prepare_query(table='stocks')
        return self._request(query)
