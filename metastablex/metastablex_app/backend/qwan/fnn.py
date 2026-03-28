import numpy as np
from scipy.spatial import KDTree

def false_nearest_neighbors(series, max_dim=10, tau=2):

    series = np.array(series)
    N = len(series)

    fnn_percent = []

    for dim in range(1, max_dim):

        # embedding
        embedded = np.array([
            [series[i + j*tau] for j in range(dim)]
            for i in range(N - dim*tau)
        ])

        tree = KDTree(embedded)

        false_count = 0

        for i, point in enumerate(embedded):

            dist, idx = tree.query(point, k=2)
            neighbor = embedded[idx[1]]

            if dim < max_dim:
                try:
                    next_dist = abs(
                        series[i + dim*tau] - series[idx[1] + dim*tau]
                    )
                except:
                    continue

                if dist[1] == 0:
                    continue

                ratio = next_dist / dist[1]

                if ratio > 10:
                    false_count += 1

        fnn_percent.append(false_count / len(embedded))

    return fnn_percent

def optimal_dimension(series):

    fnn = false_nearest_neighbors(series)

    for i, val in enumerate(fnn):
        if val < 0.01:
            return i + 1

    return len(fnn)
