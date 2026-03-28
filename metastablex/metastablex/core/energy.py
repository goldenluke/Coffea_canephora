import numpy as np
from scipy.stats import gaussian_kde

def energia_livre(serie):
    kde = gaussian_kde(serie)
    xs = np.linspace(serie.min(), serie.max(), 100)
    prob = kde(xs)
    energia = -np.log(prob)
    return xs, energia
