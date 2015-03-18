#!/usr/bin/env python
# encoding: utf-8
"""
Use Yahoo finance API to retrieve key financial (inspiration and thanks to http://www.gummy-stuff.org/Yahoo-data.htm)
"""

import urllib
import csv
from hedge import snp500

items = [
    ['l1', 'Price'], # strictly this is ask price
    ['y', 'Dividend Yield'],
    ['r', 'Price/Earnings'],
    ['e', 'Earnings/Share'],
    ['b4', 'Book Value'],
    ['j', '52 week low'],
    ['k', '52 week high'],
    ['j1', 'Market Cap'],
    ['j4', 'EBITDA'],
    ['p5', 'Price/Sales'],
    ['p6', 'Price/Book']
]
params = ''.join([ x[0] for x in items ])

sp500_index = snp500.SNP500Index()


outrows = [ list(row) for row in sp500_index.stocks ]

outrows[0] += [ item[1] for item in items ] + ['SEC Filings']

symbols = [ stock.Symbol for stock in sp500_index.stocks ]

url = 'http://finance.yahoo.com/d/quotes.csv?'
edgar = 'http://www.sec.gov/cgi-bin/browse-edgar?action=getcompany&CIK='

def _correctToBillions(item):
   if item.endswith('M'):
       return float(item[:-1]) / 1000
   elif item.endswith('B'):
       return item[:-1]
   else:
       return item

def process():

    # Go through the list by 20 stocks
    for idx in range(0,500,20):

        query = url + 's=' + '+'.join(symbols[idx:idx+20]) + '&f=' + params
        fo = urllib.urlopen(query)
        rows = [ line.split(',') for line in fo.read().split('\r\n')[:-1] ]

        for count, row in enumerate(rows):

            realidx = idx + count + 1
            # change n/a to empty cell
            row = [ x.replace('N/A', '') for x in row ]
            # market cap and ebitda have 'B' or 'M' in them sometimes
            row[7] = _correctToBillions(row[7])
            row[8] = _correctToBillions(row[8])
            # add the edgar link
            row.append(edgar + symbols[realidx-1])
            outrows[realidx] = outrows[realidx] + row

        print('Processed: %s rows' % (idx + 20))

    with open('constituents-financials.csv', 'w') as f:
        writer = csv.writer(f, lineterminator='\n')
        writer.writerows(outrows)

if __name__ == '__main__':
    process()
