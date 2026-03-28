import numpy as np
import itertools

def permutation_entropy(series, order=3, delay=1):

    n = len(series)
    permutations = list(itertools.permutations(range(order)))
    counts = dict.fromkeys(permutations, 0)

    for i in range(n - delay*(order-1)):
        window = series[i:(i + delay*order):delay]
        key = tuple(np.argsort(window))
        counts[key] += 1

    probs = np.array(list(counts.values()), dtype=float)
    probs /= probs.sum()

    probs = probs[probs > 0]

    return -np.sum(probs * np.log(probs))
