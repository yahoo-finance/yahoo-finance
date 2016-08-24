=============
yahoo-finance
=============

Python module to get stock data from Yahoo! Finance

.. image:: https://travis-ci.org/lukaszbanasiak/yahoo-finance.svg?branch=master
    :target: https://travis-ci.org/lukaszbanasiak/yahoo-finance

Install
-------

From PyPI with pip:

.. code:: bash

    $ pip install yahoo-finance

From development repo (requires git)

.. code:: bash

    $ git clone git://github.com/lukaszbanasiak/yahoo-finance.git
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

Summary information for our example

.. code:: python

    >>> from pprint import pprint
    >>> pprint(yahoo.get_info())
    {u'FullTimeEmployees': u'12200',
     u'Industry': u'Internet Information Providers',
     u'Sector': u'Technology',
     u'end': u'2014-05-03',
     u'start': u'1996-04-12',
     u'symbol': u'YHOO'}

Avalible methods

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
- ``get_info()``
- ``get_name()``
- ``refresh()``

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
