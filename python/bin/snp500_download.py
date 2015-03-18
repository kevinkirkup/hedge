#!/usr/bin/env python
# encoding: utf-8
"""
Script to download the historical data for the S&P 500 stock index
http://www.thealgoengineer.com/2014/download_sp500_data/
"""

from hedge import snp500
import pytz
import pandas as pd

from datetime import datetime
from pandas.io.data import DataReader

from hedge import yahoo

START = datetime(1900, 1, 1, 0, 0, 0, 0, pytz.utc)
END = datetime.today().utcnow()


def download_ohlc(sector_tickers, start, end):
    '''
    Download the Opening High/Low for the specific stocks
    '''

    sector_ohlc = {}

    for sector, tickers in sector_tickers.iteritems():

        print 'Downloading data from Yahoo for %s sector' % sector

        sector_ohlc[sector] = yahoo.interval_panel(tickers, yahoo.TradingInterval.Daily, start, end)

    print 'Finished downloading data'
    return sector_ohlc


def store_HDF5(sector_ohlc, path):
    '''
    Store the sector to data to HDF5 data file
    '''

    with pd.get_store(path) as store:
        for sector, ohlc in sector_ohlc.iteritems():
            store[sector] = ohlc


def get_snp500():
    '''
    Download S&P 500 stock data
    '''

    sector_tickers = snp500.SNP500Index().by_sector()

    sector_ohlc = download_ohlc(sector_tickers, START, END)
    store_HDF5(sector_ohlc, 'snp500.h5')

if __name__ == '__main__':
    get_snp500()
