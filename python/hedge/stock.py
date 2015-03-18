#!/usr/bin/env python
# encoding: utf-8
"""
Generic stock functions
"""

class Stock(object):
    """
    Generic Stock information
    """

    def __init__(self, symbol, name, sector):
        super(Stock, self).__init__()

        self.symbol = symbol
        self.name = name
        self.sector = sector
