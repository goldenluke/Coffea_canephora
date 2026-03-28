import numpy as np

def lyapunov_exponent(ts):
    ts = np.array(ts)

    diffs = np.abs(np.diff(ts))

    diffs = diffs[diffs > 0]

    if len(diffs) < 2:
        return 0

    return np.mean(np.log(diffs))
