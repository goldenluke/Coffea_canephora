import numpy as np

def coarse_grain(ts, scale):

    ts = np.array(ts)

    n = len(ts)//scale

    if n < 2:
        return ts

    return ts[:n*scale].reshape(n,scale).mean(axis=1)


def multiscale_series(ts, scales):

    series = []

    for s in scales:
        series.append(coarse_grain(ts,s))

    return series
