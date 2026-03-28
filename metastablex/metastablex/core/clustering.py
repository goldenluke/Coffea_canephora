import numpy as np
from sklearn.cluster import KMeans

def cluster_temporal(serie, window=5):
    X = []

    for i in range(len(serie) - window):
        sub = serie.iloc[i:i+window]
        X.append([sub.mean(), sub.std()])

    model = KMeans(n_clusters=3)
    return model.fit_predict(np.array(X))
