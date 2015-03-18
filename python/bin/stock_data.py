#!/usr/bin/env python
# encoding: utf-8
"""
Download the dividend information for the specified stock and time interval
"""

import argparse
import pytz

import pandas as pd

from hedge import yahoo

from datetime import datetime

##################################################
# Create the option parser
##################################################
parser = argparse.ArgumentParser(
    description="Download the stock data for the specified stock and time interval.")

parser.add_argument("stocks", nargs="+", action="store", help="Stocks to fetch", metavar="SYM")
parser.add_argument("--start", "-s", action="store", help="Start Date", metavar="MM-DD-YYYY")
parser.add_argument("--end", "-e", action="store", help="End Date", metavar="MM-DD-YYYY")

group = parser.add_mutually_exclusive_group(required=True)
group.add_argument(
    "--interval", "-i",
    choices=['daily', 'weekly', 'monthly'],
    default='daily',
    action="store",
    help="Stock Price Interval")
group.add_argument(
    "--dividend", "-d",
    action='store_true',
    help="Request Dividend information")

args = parser.parse_args()

# Start Data
if args.start:
    start = datetime.strptime(args.start, '%m-%d-%Y')
else:
    start = datetime(1900, 1, 1, 0, 0, 0, 0, pytz.utc)

# End Date
if args.end:
    end = datetime.strptime(args.end, '%m-%d-%Y')
else:
    end = datetime.today().utcnow()

# The sampling interval
if args.dividend:
    result = yahoo.dividend_frame(args.stocks, start, end)

else:
    interval = yahoo.TradingInterval.from_string(args.interval)
    result = yahoo.interval_panel(args.stocks, interval, start, end)
    result = result.to_frame()

print result
