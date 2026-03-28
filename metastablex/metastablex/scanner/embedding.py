from sklearn.decomposition import PCA
import numpy as np

def embed_vectors(vectors, dim=2):

    X = np.array(vectors)

    model = PCA(n_components=dim)

    return model.fit_transform(X)
