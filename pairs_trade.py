#Imports
from load_pkl import get_data
import numpy as np
import statsmodels
import statsmodels.api as sm
from statsmodels.tsa.stattools import coint, adfuller
import pandas as pd
import matplotlib.pyplot as plt
from cointegration_functions import pair_check, pairs_list

DATA_TRESHOLD = 7000
#TODOS

#TODO 1: Clean the data
#TODO 2: Find the optimal amount of data to be used to check for co-integration
#TODO 3: Write a function that removes the effect of the market before checking for co-integration
#TODO 4: write the code for the very last part - executing the trade


# A list of stock symbols that you want, if the symbol is invalid, the system will ignore
stock_list = ["PEP", "KO", "SPY", "BTC-USD", "IBM", "DJI", "JPM", "GS"]
stock_pairs = pairs_list(l = stock_list)

# Choice of headers from ['Adj Close', 'Close', 'Open', 'Volume', 'Low', 'High']
headers = ['Close']

# Getting the stock data
stock_data = get_data(stock_list, headers)
stock_data = stock_data["Close"]

# Checking for co-integration for GS and JPM

# GS_data = stock_data["GS"][6000:]
# JPM_data = stock_data["JPM"][6000:]

# print(pair_check(y=pepsi_data, x= coke_data))

# Wierd phenomenon - for data [6000:0] when y= JPM and x= GS the p-value is 0.5081006986065552
# when I change the palaces then p-value also changes, it becomes 0.4523076847220332


#In order to check all possible pairs from the stock_list execute the following

for pair in stock_pairs:
    y_ticker = pair[0]
    x_ticker = pair[1]
    y_data = stock_data[y_ticker][DATA_TRESHOLD:]
    x_data = stock_data[x_ticker][DATA_TRESHOLD:]
    print(pair_check(y=y_data, x=x_data))
