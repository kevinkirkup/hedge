#!/usr/bin/env Rscript

suppressPackageStartupMessages(library(argparse))
suppressPackageStartupMessages(library("quantmod"))

##################################################
# Create the parser
##################################################
parser <- ArgumentParser()

# Add our options
parser$add_argument("-S", "--symbols", action="store", nargs="+", default="AAPL, CSCO", help="List of stock symbols")
parser$add_argument("-f", "--file", action="store", nargs=1, default="", help="File with a list of stock symbols. One per line.")
parser$add_argument("-s", "--start", action="store", default="1900-01-01", help="The start date")
parser$add_argument("-e", "--end", action="store", help="The end date")
parser$add_argument("-o", "--output", action="store", default="stock_chart.pdf", help="Path to store the output.")

args <- parser$parse_args()

file <- args$file

if (file.access(file) == -1) {
  symbols <- args$symbols

} else {
  symbols <- readLines(file)
}

# Check the output file extension

# Create the file
pdf(args$output)

# Read the stock symbols from the command line
Symbols <- unlist(strsplit(as.character(symbols), split=",|, "))

Stocks <- lapply(Symbols, function(i) {

  s <- getSymbols(i, auto.assign=FALSE)

  candleChart(s, subset='last 6 months', name=i, bar.type="ohlc", theme=chartTheme('black'))
})
