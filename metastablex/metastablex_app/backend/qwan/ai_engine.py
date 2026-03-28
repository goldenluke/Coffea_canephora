import numpy as np
from sklearn.cluster import KMeans

def cluster_states(data, k=3):
    if len(data) < k:
        return [0]*len(data)

    kmeans = KMeans(n_clusters=k, n_init=5)
    labels = kmeans.fit_predict(data)
    return labels.tolist()

def control_policy(H, I, Phi):
    # heurística inteligente simples

    # sistema muito estável → aumentar instabilidade
    if Phi < 0.2:
        return {"k": 3.5, "noise": 0.02}

    # sistema caótico → reduzir ruído
    if I > 1.5:
        return {"noise": 0.005}

    # regime interessante → manter
    return {}
