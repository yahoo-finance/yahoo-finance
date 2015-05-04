import datetime
import sys
import unittest

if sys.version_info < (2, 7):
    from unittest2 import main as test_main, SkipTest, TestCase
else:
    from unittest import main as test_main, SkipTest, TestCase

from yahoo_finance import Currency, Share


class TestShare(TestCase):
    def test_yhoo(self):
        yahoo = Share("YHOO")
        # assert that these are float-like
        float(yahoo.get_open())
        float(yahoo.get_price())

    #def test_info(self):
    #    yahoo = Share("YHOO")
    #    info = yahoo.get_info()
    #    self.assertEqual(info["Sector"], "Technology")

    def test_historical(self):
        yahoo = Share("YHOO")
        historical = yahoo.get_historical("2014-04-25", "2014-04-29")
        self.assertEqual(len(historical), 3)
        expected = {
            'Adj_Close': '35.83',
            'Close': '35.83',
            'Date': '2014-04-29',
            'High': '35.89',
            'Low': '34.12',
            'Open': '34.37',
            'Symbol': 'YHOO',
            'Volume': '28736000'
        }
        self.assertDictEqual(historical[0], expected)

class TestCurrency(TestCase):
    def test_eurpln(self):
        eur_pln = Currency("EURPLN")
        # assert these are float-like
        float(eur_pln.get_bid())
        float(eur_pln.get_ask())
        float(eur_pln.get_rate())

    def test_eurpln_date(self):
        eur_pln = Currency("EURPLN")
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
