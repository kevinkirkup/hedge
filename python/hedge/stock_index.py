
#!/usr/bin/env python
# encoding: utf-8
"""
Functions Related to S&P 500 index
"""
from collections import defaultdict

class StockIndex(object):
    """
    Stock Index and helper function
    """
    def __init__(self):
        super(StockIndex, self).__init__()

        self.stocks = []

    def by_sector(self):
        """
        Sort the list of Stocks by their sectors

        :returns: Dictionary of Stocks by Sector

        """

        sector_dict = defaultdict(list)

        for s in self.stocks:
            sector_dict[s.Sector].append(s.Symbol)

        return sector_dict
