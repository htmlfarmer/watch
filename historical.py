import datetime
import locale  # text string parsing to number (float)
from request import REQUEST
import xml.etree.ElementTree as ElementTree
import re
from file import READ
from website import Website

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

symbol = "PBR"
url = "https://query1.finance.yahoo.com/v7/finance/download/" + symbol + "?period1=965865600&period2=1606780800&interval=1d&events=history&includeAdjustedClose=true"

sp500 = pd.read_csv('historical/^GSPC.csv')

text = REQUEST(url)

output_path = "quotes"
def make_filename(ticker_symbol, directory="S&P"):
    return output_path + "/" + directory + "/" + ticker_symbol + ".csv"

def pull_historical_data(ticker_symbol, directory="S&P"):
    try:
        urllib.urlretrieve(make_url(ticker_symbol), make_filename(ticker_symbol, directory))
    except urllib.ContentTooShortError as e:
        outfile = open(make_filename(ticker_symbol, directory), "w")
        outfile.write(e.content)
        outfile.close()