import pandas as pd
from statsmodels.tsa.stattools import adfuller
import statsmodels.api as sm
import numpy as np

def check_for_stationarity(X, cutoff=0.05):
    # H_0 in adfuller is unit root exists (non-stationary)
    # We must observe significant p-value to convince ourselves that the series is stationary
    pvalue = adfuller(X)[1]
    if pvalue < cutoff:
        # print('p-value = ' + str(pvalue) + ' The series ' + X.name +' is likely stationary.')
        return True
    else:
        # print('p-value = ' + str(pvalue) + ' The series ' + X.name +' is likely non-stationary.')
        return False


def regress(Y,X): #Regress Y on X, returns a dictionary with 'residuals' and 'coeffs' as keys
    X_temp = X
    X = sm.add_constant(X)
    model = sm.OLS(Y,X)
    results = model.fit()
    residual = Y -  (results.params[1] * X_temp + results.params[0])
    d = dict()
    d['residuals'] = residual
    d['coeffs'] = results.params
    return d

def pair_check(y: pd.Series,x: pd.Series): #the passed arguments are the close prices of the stocks. Regressed y on x.
    y_return = y.pct_change(1)[1:]
    x_return = x.pct_change(1)[1:]
    y_return_stationarity = check_for_stationarity(y_return)
    x_return_stationarity = check_for_stationarity(x_return)
    if y_return_stationarity == True and x_return_stationarity == True:
        # Computing cumulative returns
        y_cum_return = y_return.cumsum()
        x_cum_return = x_return.cumsum()
        regression_results = regress(Y= y_cum_return, X = x_cum_return)
        residual = regression_results["residuals"]
        residual_stationarity = check_for_stationarity(residual)
        if residual_stationarity == True:
            print(f"The pair {y.name} and {x.name} are co-integrated")
            return True
            #TODO 1: return coefficient of regression and the bias.

            # return {"is_pair": True, "coefficients_of_regression": regression_results.params,
            # "residuals": residual}
            # Do I need to return anything else?

        else:
            print(f"The pair {y.name} and {x.name} are not co-integrated and the p-value is {adfuller(residual)[1]}")
            #maybe it is a good idea to return the p-value
            return False


    else:
        if y_return_stationarity == False and x_return_stationarity == False:
            print("the returns of both stocks is not stationary")
        elif y_return_stationarity == False:
            print(f"the returns of {y.name} stocks is not stationary")
        elif x_return_stationarity == False:
            print(f"the returns of {x.name} stocks is not stationary")
        return False


def pairs_list(l: list):
    pairs = []
    for i in range(len(l)):
        for j in range(i+1,len(l)):
            pairs.append( (l[i],l[j]) )
    return pairs


def pair_check_log(y: pd.Series,x: pd.Series):
    log_y = np.log(y)
    log_x = np.log(x)
    log_y_stationarity = check_for_stationarity(log_y)
    log_x_stationarity = check_for_stationarity(log_x)
    if log_y_stationarity == False and log_x_stationarity == False:
        #Regressing log_y on log_x
        regression_results = regress(Y=log_y, X=log_x)
        residual = regression_results["residuals"]
        residual_stationarity = check_for_stationarity(residual)
        if residual_stationarity == True:
            print(f"The pair {y.name} and {x.name} are co-integrated")
            result = {"is_pair": True, "coefficients_of_regression": regression_results['coeffs'],
            "residuals": residual}
            return result

        else:
            print(f"The pair {y.name} and {x.name} are not co-integrated and the p-value is {adfuller(residual)[1]}")
            # maybe it is a good idea to return the p-value
            return False


    else:
        if log_y_stationarity == True and log_x_stationarity == True:
            print("the log close prices for both stocks are stationary")
        elif log_y_stationarity == True:
            print(f"the log close price for {y.name} stock is stationary")
        elif log_x_stationarity == True:
            print(f"the log close price for {x.name} stock is stationary")
        return False

