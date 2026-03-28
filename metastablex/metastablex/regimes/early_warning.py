import numpy as np
import pandas as pd

def autocorrelation_lag1(ts):
    ts = pd.Series(ts)
    return ts.autocorr(lag=1)

def rolling_variance(ts, window=20):
    ts = pd.Series(ts)
    return ts.rolling(window).var().to_numpy()

def critical_slowing_down(ts, window=20):
    ts = pd.Series(ts)

    ac1 = ts.rolling(window).apply(lambda x: pd.Series(x).autocorr(lag=1))
    var = ts.rolling(window).var()

    return {
        "ac1": ac1.to_numpy(),
        "variance": var.to_numpy()
    }

def flickering_indicator(ts):
    ts = np.array(ts)

    mean = np.mean(ts)
    std = np.std(ts)

    return np.sum(np.abs(ts - mean) > 2 * std)
