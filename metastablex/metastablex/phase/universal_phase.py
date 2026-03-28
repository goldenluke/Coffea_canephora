import numpy as np
from sklearn.cluster import KMeans

class UniversalPhaseDiagram:

    def __init__(self, n_classes=5):
        self.model = KMeans(n_clusters=n_classes)

    def fit(self, rg_points):

        X = rg_points[:, :3]  # (C,S,E)

        self.model.fit(X)

    def classify(self, points):

        return self.model.predict(points[:, :3])
