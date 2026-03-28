import numpy as np
from sklearn.metrics import mutual_info_score

def compute_mutual_information(series, max_tau=50):

    series = np.array(series)
    mi = []

    for tau in range(1, max_tau):

        x = series[:-tau]
        y = series[tau:]

        bins = np.histogram_bin_edges(series, bins=20)

        x_binned = np.digitize(x, bins)
        y_binned = np.digitize(y, bins)

        mi_val = mutual_info_score(x_binned, y_binned)
        mi.append(mi_val)

    return mi

def optimal_tau(series):

    mi = compute_mutual_information(series)

    for i in range(1, len(mi)-1):
        if mi[i] < mi[i-1] and mi[i] < mi[i+1]:
            return i

    return 1
