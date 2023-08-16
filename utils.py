from polygon import RESTClient
from polygon.rest import models
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import statsmodels.api as sm
from statsmodels.graphics.tsaplots import plot_pacf
from statsmodels.graphics.tsaplots import plot_acf

from cointegration_functions import check_for_stationarity

client = RESTClient("RcARxdOZUV3tCcMYO5WUWYDHIi6dTmJk") # api_key is used

def get_aggs(symbol_name, start_date="2020-04-04", end_date="2023-04-04"):
    aggs = client.get_aggs(
        symbol_name,
        1,
        "day",
        start_date,
        end_date
    )
    return aggs

def close_price_from_aggs(aggs):
    close = []
    for i in range(len(aggs)):
        close.append(aggs[i].close)
    return close

def plot_price_data(A_close: list[int], B_close: list[object], name_A, name_B, title="Price Data"):
    A_close = pd.Series(A_close, name=name_A)
    B_close = pd.Series(B_close, name=name_B)
    plt.plot(A_close, 'b', label=name_A)
    plt.plot(B_close, 'r', label=name_B)
    plt.legend()
    plt.title(title)
    plt.show()

def fit_OLS_model(log_close_A, log_close_B, remain_days=255):
    '''

    :param log_close_A: log close price A
    :param log_close_B: log close price B
    :param remain_days: how many days remained for testing, only use the rest days for training
    :return: residuals, coefficients
    '''
    A = log_close_A[:len(log_close_A) - remain_days]
    B = log_close_B[:len(log_close_B) - remain_days]
    A_temp = A
    A = sm.add_constant(A)
    model = sm.OLS(B, A)
    resultsOLS = model.fit()
    const = resultsOLS.params[0]
    coefficient = resultsOLS.params[1]
    residuals = B - (coefficient * A_temp + const)
    return {
        "const": const,
        "coefficient": coefficient,
        "residuals": residuals
    }

if __name__ == "__main__":

    # Get aggs and close prices
    aggs_pep = get_aggs("PEP", start_date="2020-04-04", end_date="2023-04-04")
    aggs_ko = get_aggs("KO", start_date="2020-04-04", end_date="2023-04-04")
    pep_close = close_price_from_aggs(aggs_pep)
    ko_close = close_price_from_aggs(aggs_ko)

    # Plot price
    plot_price_data(pep_close, ko_close, "Pepsi Closing Price", "Coke Closing Price")
    # Plot log price
    log_pep_close = np.log(pep_close)
    log_ko_close = np.log(ko_close)
    plot_price_data(log_pep_close, log_ko_close, "log Pepsi Closing Price", "log Coke Closing Price", title="Log Price Data")
    return_dict = fit_OLS_model(log_pep_close, log_ko_close, remain_days=255)
    const = return_dict["const"]
    coefficient = return_dict["coefficient"]
    residuals = return_dict["residuals"]

    # Plot ACF and PACF
    acf = plot_acf(residuals, lags=35)
    acf.show()
    pacf = plot_pacf(residuals, lag=35)
    pacf.show()

    # train and test data split
    train_data = residuals
    test_data = log_pep_close[-255: ] - (coefficient * log_ko_close[-255: ] + const)

    # TODO: Fit AR(1) model to get spread
    # TODO: start trading


