import numpy as np
from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import RBF

class RegimeField:

    def __init__(self):

        kernel = RBF(length_scale=0.5)

        self.model = GaussianProcessRegressor(
            kernel=kernel,
            alpha=1e-3
        )

    def fit(self,X,y):

        self.model.fit(X,y)

    def predict(self,X):

        return self.model.predict(X)
