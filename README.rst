=============
yhoo-finance
=============

Python module to get stock data from Yahoo! Finance

.. image:: https://travis-ci.org/lukaszbanasiak/yahoo-finance.svg?branch=master
    :target: https://travis-ci.org/lukaszbanasiak/yahoo-finance

Legal disclaimer
----------------
Yahoo!, Y!Finance, and Yahoo! finance are registered trademarks of Yahoo, Inc.

yhoo-finance is not affiliated, endorsed, or vetted by Yahoo, Inc. It's an open-source tool that uses Yahoo's publicly available APIs, and is intended for research and educational purposes.

You should refer to Yahoo!'s terms of use (https://policies.yahoo.com/us/en/yahoo/terms/product-atos/apiforydn/index.htm, https://legal.yahoo.com/us/en/yahoo/terms/otos/index.html, https://policies.yahoo.com/us/en/yahoo/terms/index.htm) for details on your rights to use the actual data downloaded. Remember - the Yahoo! finance API is intended for personal use only.

Know issues
-----------
Yahoo! Finance backend is http://datatables.org/. If this service is down or
has network problems you will receive errors from group YQL*,
eg. ``YQLQueryError``.

You can monitor this service via https://www.datatables.org/healthchecker/

More details https://github.com/lukaszbanasiak/yahoo-finance/issues/44

Install
-------

From PyPI with pip:

.. code:: bash

    $ pip install yahoo-finance

From development repo (requires git)

.. code:: bash

    $ git clone git://github.com/lukaszbanasiak/yhoo-finance.git
    $ cd yahoo-finance
    $ python setup.py install

Usage examples
--------------

Get shares data
^^^^^^^^^^^^^^^

Example: Yahoo! Inc. (``YHOO``)

.. code:: python

    >>> from yahoo_finance import Share
    >>> yahoo = Share('YHOO')
    >>> print yahoo.get_open()
    '36.60'
    >>> print yahoo.get_price()
    '36.84'
    >>> print yahoo.get_trade_datetime()
    '2014-02-05 20:50:00 UTC+0000'

Refresh data from market

.. code:: python

    >>> yahoo.refresh()
    >>> print yahoo.get_price()
    '36.87'
    >>> print yahoo.get_trade_datetime()
    '2014-02-05 21:00:00 UTC+0000'

Historical data

.. code:: python

    >>> print yahoo.get_historical('2014-04-25', '2014-04-29')
    [{u'Volume': u'28720000', u'Symbol': u'YHOO', u'Adj_Close': u'35.83', u'High': u'35.89', u'Low': u'34.12', u'Date': u'2014-04-29', u'Close': u'35.83', u'Open': u'34.37'}, {u'Volume': u'30422000', u'Symbol': u'YHOO', u'Adj_Close': u'33.99', u'High': u'35.00', u'Low': u'33.65', u'Date': u'2014-04-28', u'Close': u'33.99', u'Open': u'34.67'}, {u'Volume': u'19391100', u'Symbol': u'YHOO', u'Adj_Close': u'34.48', u'High': u'35.10', u'Low': u'34.29', u'Date': u'2014-04-25', u'Close': u'34.48', u'Open': u'35.03'}]

More readable output :)

.. code:: python

    >>> from pprint import pprint
    >>> pprint(yahoo.get_historical('2014-04-25', '2014-04-29'))
    [{u'Adj_Close': u'35.83',
      u'Close': u'35.83',
      u'Date': u'2014-04-29',
      u'High': u'35.89',
      u'Low': u'34.12',
      u'Open': u'34.37',
      u'Symbol': u'YHOO',
      u'Volume': u'28720000'},
     {u'Adj_Close': u'33.99',
      u'Close': u'33.99',
      u'Date': u'2014-04-28',
      u'High': u'35.00',
      u'Low': u'33.65',
      u'Open': u'34.67',
      u'Symbol': u'YHOO',
      u'Volume': u'30422000'},
     {u'Adj_Close': u'34.48',
      u'Close': u'34.48',
      u'Date': u'2014-04-25',
      u'High': u'35.10',
      u'Low': u'34.29',
      u'Open': u'35.03',
      u'Symbol': u'YHOO',
      u'Volume': u'19391100'}]

Available methods

- ``get_price()``
- ``get_change()``
- ``get_percent_change()``
- ``get_volume()``
- ``get_prev_close()``
- ``get_open()``
- ``get_avg_daily_volume()``
- ``get_stock_exchange()``
- ``get_market_cap()``
- ``get_book_value()``
- ``get_ebitda()``
- ``get_dividend_share()``
- ``get_dividend_yield()``
- ``get_earnings_share()``
- ``get_days_high()``
- ``get_days_low()``
- ``get_year_high()``
- ``get_year_low()``
- ``get_50day_moving_avg()``
- ``get_200day_moving_avg()``
- ``get_price_earnings_ratio()``
- ``get_price_earnings_growth_ratio()``
- ``get_price_sales()``
- ``get_price_book()``
- ``get_short_ratio()``
- ``get_trade_datetime()``
- ``get_historical(start_date, end_date)``
- ``get_name()``
- ``refresh()``
- ``get_percent_change_from_year_high()``
- ``get_percent_change_from_year_low()``
- ``get_change_from_year_low()``
- ``get_change_from_year_high()``
- ``get_percent_change_from_200_day_moving_average()``
- ``get_change_from_200_day_moving_average()``
- ``get_percent_change_from_50_day_moving_average()``
- ``get_change_from_50_day_moving_average()``
- ``get_EPS_estimate_next_quarter()``
- ``get_EPS_estimate_next_year()``
- ``get_ex_dividend_date()``
- ``get_EPS_estimate_current_year()``
- ``get_price_EPS_estimate_next_year()``
- ``get_price_EPS_estimate_current_year()``
- ``get_one_yr_target_price()``
- ``get_change_percent_change()``
- ``get_dividend_pay_date()``
- ``get_currency()``
- ``get_last_trade_with_time()``
- ``get_days_range()``
- ``get_year_range()``



Get currency data
^^^^^^^^^^^^^^^^^

Example: EUR/PLN (``EURPLN=X``)

.. code:: python

    >>> from yahoo_finance import Currency
    >>> eur_pln = Currency('EURPLN')
    >>> print eur_pln.get_bid()
    '4.2007'
    >>> print eur_pln.get_ask()
    '4.2091'
    >>> print eur_pln.get_rate()
    '4.2049'
    >>> print eur_pln.get_trade_datetime()
    '2014-03-05 11:23:00 UTC+0000'

Refresh data from market

.. code:: python

    >>> eur_pln.refresh()
    >>> print eur_pln.get_rate()
    '4.2052'
    >>> print eur_pln.get_trade_datetime()
    '2014-03-05 11:27:00 UTC+0000'

Avalible methods

- ``get_bid()``
- ``get_ask()``
- ``get_rate()``
- ``get_trade_datetime()``
- ``refresh()``

Requirements
------------

See ``requirements.txt``
