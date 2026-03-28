import numpy as np

def phase_space(ts, delay=1):

    ts = np.array(ts)

    x = ts[:-delay]
    y = ts[delay:]

    return x, y
