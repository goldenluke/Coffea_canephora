import numpy as np

def takens_embedding(series, dim=3, tau=2):

    N = len(series)

    if N < dim * tau:
        return None

    embedded = []

    for i in range(N - dim*tau):
        point = [series[i + j*tau] for j in range(dim)]
        embedded.append(point)

    return np.array(embedded)
