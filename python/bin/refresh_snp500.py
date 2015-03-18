#!/usr/bin/env python
# encoding: utf-8
"""
Functions Related to S&P 500 index
"""
import argparse
import csv

import urllib2
import os
import sys

from bs4 import BeautifulSoup

SITE = "http://en.wikipedia.org/wiki/List_of_S%26P_500_companies"


def download(filepath):
    '''
    Scrape the list of S&P 500 Stocks and their sectors from Wikipedia
    '''

    hdr = {'User-Agent': 'Mozilla/5.0'}
    req = urllib2.Request(SITE, headers=hdr)
    page = urllib2.urlopen(req)
    soup = BeautifulSoup(page)

    table = soup.find('table', {'class': 'wikitable sortable'})

    fieldnames = ['Symbol', 'Name', 'Sector']

    with open(filepath, 'wb') as csvfile:

        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        for row in table.findAll('tr'):

            col = row.findAll('td')

            if len(col) > 0:

                symbol = str(col[0].string.strip())
                name = str(col[1].string.strip())
                sector = str(col[3].string.strip()).lower().replace(' ', '_')

                writer.writerow({
                    'Symbol': symbol,
                    'Name': name,
                    'Sector': sector
                })


##################################################
# Main
##################################################
parser = argparse.ArgumentParser(
    description="Script to download the S&P 500 data")

parser.add_argument("--output", "-o", default="SNP500.csv", action="store", help="Output file path", metavar="FILE")

args = parser.parse_args()

# Check the file extension if a filename was specified
extension = os.path.basename(args.output).split('.')[1]

if extension.lower() != "csv":
    print "Must be a CSV file, %s specified!\n" % args.output
    parser.print_help()
    sys.exit(1)

download(args.output)

