#!/usr/bin/env python
# encoding: utf-8
"""
Yahoo Finance API
"""

import urllib
import pandas as pd

from io import StringIO

#BASE_URL = "http://ichart.yahoo.com/x?"
BASE_URL = "http://ichart.yahoo.com/table.csv"
STOCK_QUERY_TEMPLATE = "{base_url}?s={symbol}&a={start.month}&b={start.day}&c={start.year}&d={end.month}&e={end.day}&f={end.year}&g={interval}&ignore=.csv"


class TradingInterval(object):
    """
    Class for the availble trading intervals
    """

    Daily = "d"
    Weekly = "w"
    Monthly = "m"
    Dividend = "v"

    @staticmethod
    def from_string(name):
        """
        Convert the specified string to an interval value

        :name: The name to describe the interval
        :returns: Value for the Interval

        """

        result = TradingInterval.Dividend

        if name.lower() == "daily":
            result = TradingInterval.Daily

        elif name.lower() == "weekly":
            result = TradingInterval.Weekly

        elif name.lower() == "monthly":
            result = TradingInterval.Monthly

        return result


def download_dividends(symbol, start, end):
    """
    Download the dividend information for the specified Stock and time interval

    :symbol: The Stock Symbol
    :start: The start date
    :end: The end date
    :returns: DataFrame containing dividend information for the specified time and interval

    """
    return download_data(symbol, start, end, TradingInterval.Dividend)


def download_data(symbol, start, end, interval):
    """
    Download the stock data for the specified Stock Symbol and time interval

    :symbol: The Stock Symbol
    :start: The start date
    :end: The end date
    :interval: The TradingInterval
    :returns: DataFrame containing dividend information for the specified time and interval

    """
    query = STOCK_QUERY_TEMPLATE.format(base_url=BASE_URL, symbol=symbol, start=start, end=end, interval=interval)

    result = urllib.urlopen(query)
    data = unicode(result.read())

    data_io = StringIO(data)

    df = pd.DataFrame.from_csv(data_io)

    return df

def adjust_panel(panel):
    """
    Adjust the Stock data based on the Adjusted Close

    :panel: The panel to modify
    :returns: Adjusted panel

    """

    p = panel.swapaxes('items', 'minor')

    for item in ['Open', 'High', 'Low']:

        # Adj Close / Close = Stock Split and Dividend Adjustment
        p[item] = p[item] * p['Adj Close'] / p['Close']

    p.rename(items={'Open': 'open',
                    'High': 'high',
                    'Low': 'low',
                    'Adj Close': 'close',
                    'Volume': 'volume'},
             inplace=True)

    return p.drop(['Close'])


def interval_panel(symbols, interval, start, end):
    """
    Create a Pandas Panel for the specific stock symbol contain the stock quote
    information for the specified date range

    :symbols: List of Stock Symbols
    :interval: Data interval for query
    :start: The start date
    :end: The end date
    :returns: Combined Data

    """
    dd = {}

    # Query for the stock information
    for s in symbols:
        dd[s] = download_data(s, start, end, interval)

    return adjust_panel(pd.Panel(dd))


def dividend_frame(symbols, start, end):
    """
    Create a Pandas Panel for the specific stock symbol contain the divided
    information for the specified date range

    :symbols: List of Stock Symbols
    :start: The start date
    :end: The end date
    :returns: Combined Data

    """
    dl = []

    # Query for the stock information
    for s in symbols:

        df = download_data(s, start, end, TradingInterval.Dividend)
        df.rename(columns={'Dividends': s}, inplace=True)

        # Merge them based on the Date
        dl.append(df)

    return pd.concat(dl, axis=1)


def dividend_panel(symbols, start, end):
    """
    Create a Pandas Panel for the specific stock symbol contain the divided
    information for the specified date range

    :symbols: List of Stock Symbols
    :start: The start date
    :end: The end date
    :returns: Combined Data

    """
    df = dividend_frame(symbols, start, end)

    return pd.Panel({'Dividends': df})
