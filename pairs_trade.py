#Imports
from load_pkl import get_data
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from cointegration_functions import pair_check, pairs_list, pair_check_log, check_for_stationarity
from statsmodels.tsa.arima.model import ARIMA
from sklearn.metrics import r2_score
from scipy.stats import zscore
from statsmodels.graphics.tsaplots import plot_pacf

DATA_THRESHOLD = 7000

#TODOS

#TODO 1: Clean the data
#TODO 2: Find the optimal amount of data to be used to check for co-integration
#TODO 3: Write a function that removes the effect of the market before checking for co-integration
#TODO 4: write the code for the very last part - executing the trade


# A list of stock symbols that you want, if the symbol is invalid, the system will ignore
stock_list = ["PEP", "KO", "SPY", "BTC-USD", "IBM", "JPM", "GS"]
stock_pairs = pairs_list(l = stock_list)

# Choice of headers from ['Adj Close', 'Close', 'Open', 'Volume', 'Low', 'High']
headers = ['Close']

# Getting the stock data
stock_data = get_data(stock_list, headers)
stock_data = stock_data["Close"]


# In order to check all possible pairs from the stock_list execute the following

# for pair in stock_pairs:
#     y_ticker = pair[0]
#     x_ticker = pair[1]
#     y_data = stock_data[y_ticker][DATA_THRESHOLD:]
#     x_data = stock_data[x_ticker][DATA_THRESHOLD:]
#     results = pair_check_log(y=y_data, x=x_data)
#     if type(results) != bool:
#         print(results["coefficients_of_regression"])


# IBM close price process is stationary when observed from 2010 till 2023.

# print(check_for_stationarity((stock_data["IBM"][5000:])))
#
# plt.plot(stock_data["IBM"][5000:])
# plt.show()


# Results from log approach is more intuitive, than the results with cumulative sums.

# for stock in stock_list:
#     print(stock_data[stock][DATA_THRESHOLD:])


# ------------------------- FROM THIS POINT ON EVEYRTHING IS JUST AN EXPERIMENT. CAN CONTAIN BUGS AND NON-SENSE

#BITCOIN & GS
BTC_training_data = stock_data["BTC-USD"][DATA_THRESHOLD:8200]
GS_training_data = stock_data["GS"][DATA_THRESHOLD:8200]
BTC_test_data = stock_data["BTC-USD"][8201:]
GS_test_data = stock_data["GS"][8201:]

results = pair_check_log(y=BTC_training_data, x=GS_training_data)
train_spread = results["residuals"]
# residuals_mean = np.ones(len(spread)) * np.mean(spread)
# plt.plot(np.array(spread))
# plt.plot(residuals_mean)
# plt.plot(np.ones(len(spread)) * np.std(np.array(spread)))
# plt.plot(np.ones(len(spread)) * (-np.std(np.array(spread))))
# plt.title('Spread Plot')
# plt.xlabel('Time')
# plt.ylabel('Spread')
# plt.show()

# Fitting AR(1) to the data
ar_fit = ARIMA(train_spread, order = (1,0,0)).fit()

# print(ar_fit.summary())

# ar.L1  - 0.9861
# Thus, the model is causal -> find the gamma(0) to find the variance 𝜎^2(spread)=𝜎^2(WN)/(1−𝜙^2)

# prediction = ar_fit.predict(start= len(GS_training_data)+1 , end=len(GS_training_data) + len(GS_test_data))
# test_spread = np.log(BTC_test_data) - (results["coefficients_of_regression"]["GS"] * np.log(GS_test_data) + results["coefficients_of_regression"]["const"])
# prediction.index = test_spread.index
# print(test_spread)
# plt.plot(prediction)
# plt.plot(test_spread)
# plt.show()

# Z-score calculation (w.r.t. mean)
# spread_zscore = zscore(test_spread)
# plt.plot(spread_zscore)
# plt.xlabel(xlabel="time")
# plt.ylabel(ylabel="z-score")
# plt.show()
# print(np.std(test_spread))

# Z-score calculation (w.r.t. forcast)

# # TODO: access phi instead of copy and pasting
# phi = 0.9861
# sdt_wn = None
# sdt_spread = (sdt_wn ** 2)/(1-phi**2)
# spread_zscore = (test_spread - prediction)/sdt_spread


# plot_pacf(train_spread,lags=60)
# plt.show()
