import datetime
import sys

if sys.version_info < (2, 7):
    from unittest2 import main as test_main, SkipTest, TestCase
else:
    from unittest import main as test_main, SkipTest, TestCase

from yahoo_finance import Currency, Share, edt_to_utc, get_date_range


class TestShare(TestCase):

    def setUp(self):
        self.yahoo = Share('YHOO')

    def test_yhoo(self):
        # assert that these are float-like
        float(self.yahoo.get_open())
        float(self.yahoo.get_price())

    def test_get_info(self):
        info = self.yahoo.get_info()
        self.assertEqual(info['start'], '1996-04-12')
        self.assertEqual(info['symbol'], 'YHOO')

    def test_get_historical(self):
        history = self.yahoo.get_historical('2014-04-25', '2014-04-29')
        self.assertEqual(len(history), 3)
        expected = {
            'Adj_Close': '35.830002',
            'Close': '35.830002',
            'Date': '2014-04-29',
            'High': '35.889999',
            'Low': '34.119999',
            'Open': '34.369999',
            'Symbol': 'YHOO',
            'Volume': '28736000'
        }
        self.assertDictEqual(history[0], expected)

    def test_get_historical_longer_than_1y(self):
        # issue #2
        history = self.yahoo.get_historical('2012-04-25', '2014-04-29')
        self.assertEqual(history[-1]['Date'], '2012-04-25')
        self.assertEqual(history[0]['Date'], '2014-04-29')
        self.assertEqual(len(history), 505)

    def test_get_historical_1d(self):
        # issue #7
        history = self.yahoo.get_historical('2014-04-29', '2014-04-29')
        self.assertEqual(len(history), 1)
        expected = {
            'Adj_Close': '35.830002',
            'Close': '35.830002',
            'Date': '2014-04-29',
            'High': '35.889999',
            'Low': '34.119999',
            'Open': '34.369999',
            'Symbol': 'YHOO',
            'Volume': '28736000'
        }
        self.assertDictEqual(history[0], expected)

    def test_edt_to_utc(self):
        edt = '5/26/2014 4:00pm'
        utc = '2014-05-26 20:00:00 UTC+0000'
        self.assertEqual(edt_to_utc(edt), utc)

    def test_edt_to_utc_issue15(self):
        # date string for yahoo can contains 0 rather than 12.
        # This means that it cannot be parsed with %I see GH issue #15.
        edt = '4/21/2015 0:13am'
        utc = '2015-04-21 04:13:00 UTC+0000'
        self.assertEqual(edt_to_utc(edt), utc)

    def test_get_date_range(self):
        result = [i for i in get_date_range('2012-04-25', '2014-04-29')]
        expected = [
            ('2013-04-29', '2014-04-29'),
            ('2012-04-28', '2013-04-28'),
            ('2012-04-25', '2012-04-27'),
        ]
        self.assertEqual(result, expected)


class TestCurrency(TestCase):

    def setUp(self):
        self.eur_pln = Currency('EURPLN')

    def test_eurpln(self):
        # assert these are float-like
        float(self.eur_pln.get_bid())
        float(self.eur_pln.get_ask())
        float(self.eur_pln.get_rate())

    def test_eurpln_date(self):
        eur_pln = Currency('EURPLN')
        try:
            datetime.datetime.strptime(eur_pln.get_trade_datetime(),
                                       "%Y-%m-%d %H:%M:%S %Z%z")
        except ValueError as v:
            if "bad directive" in str(v):
                raise SkipTest("datetime format checking requires the %z directive.")
            else:
                raise

if __name__ == "__main__":
    test_main()
