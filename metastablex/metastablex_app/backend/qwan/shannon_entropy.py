import numpy as np

def shannon_entropy(series, bins=30):

    hist, _ = np.histogram(series, bins=bins, density=True)
    hist = hist[hist > 0]

    return -np.sum(hist * np.log(hist))
