import numpy as np

def coarse_grain(ts, scale):

    ts = np.array(ts)

    n = len(ts)//scale

    return ts[:n*scale].reshape(n,scale).mean(axis=1)
