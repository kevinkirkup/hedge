#!/usr/bin/env Rscript

suppressPackageStartupMessages(library(argparse))
suppressPackageStartupMessages(library(quantmod))

##################################################
# Create the parser
##################################################
parser <- ArgumentParser()

# Add our options
parser$add_argument("-S", "--symbols", action="store", default="AAPL, CSCO", help="list of stock symbols")
parser$add_argument("-s", "--start", action="store", default="1900-01-01", help="The start date")
parser$add_argument("-e", "--end", action="store", help="The end date")

args <- parser$parse_args()

# Read the stock symbols from the command line
Symbols <- unlist(strsplit(as.character(args$symbols), split=",|, "))

if ( !is.null(args$start) )
  StartDate = as.Date(args$start)

if ( !is.null(args$end) )
  EndDate = as.Date(args$end)

# Get the dailyReturn data from from the specified date
Stocks <- lapply(Symbols, function(s) {
  as.xts(quarterlyReturn(na.omit(getSymbols(s, from=StartDate, auto.assign=FALSE))))
})

