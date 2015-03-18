#!/usr/bin/env python
# encoding: utf-8
"""
Functions for use with NASDAQ
"""

import csv
import pkg_resources
from hedge.stock_index import StockIndex

from collections import namedtuple

# Record format
StockData = namedtuple('StockData', 'Symbol, Name, LastSale, MarketCap, IPOYear, Sector, Industry, Summary Quote')

# The data file
DATA_FILE = pkg_resources.resource_stream('hedge', 'data/AMEX.csv')


class AmexIndex(StockIndex):
    """
    America Stock Exchange index
    """
    def __init__(self):
        super(AmexIndex, self).__init__()

        # Read the stock data from the file
        self.stocks = map(StockData._make, csv.reader(DATA_FILE))

        # Remove the Header
        self.stocks.pop(0)
