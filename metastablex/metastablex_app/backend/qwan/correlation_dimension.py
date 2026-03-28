import numpy as np
from scipy.spatial.distance import pdist

def correlation_dimension(embedded):

    if embedded is None or len(embedded) < 10:
        return None

    dists = pdist(embedded)

    r_vals = np.logspace(-3, 0, 20)
    C = []

    for r in r_vals:
        C.append(np.sum(dists < r) / len(dists))

    log_r = np.log(r_vals)
    log_C = np.log(C)

    slope = np.polyfit(log_r, log_C, 1)[0]

    return slope
