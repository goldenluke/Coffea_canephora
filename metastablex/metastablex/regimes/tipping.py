import numpy as np
import pandas as pd

def tipping_score(ts, window=30):

    ts = pd.Series(ts)

    ac1 = ts.rolling(window).apply(lambda x: pd.Series(x).autocorr(lag=1))
    var = ts.rolling(window).var()

    ac1_norm = (ac1 + 1)/2
    var_norm = var / np.nanmax(var)

    score = (ac1_norm + var_norm)/2

    return score

def detect_tipping(ts, threshold=0.7):

    score = tipping_score(ts)

    tipping_points = np.where(score > threshold)[0]

    return tipping_points, score
