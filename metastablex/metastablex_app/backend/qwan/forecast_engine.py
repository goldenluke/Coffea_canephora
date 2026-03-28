import numpy as np
from sklearn.linear_model import LinearRegression

class Forecaster:
    def __init__(self):
        self.history = []

    def update(self, value):
        self.history.append(value)
        if len(self.history) > 50:
            self.history.pop(0)

    def predict(self, steps=5):
        if len(self.history) < 5:
            return []

        X = np.arange(len(self.history)).reshape(-1,1)
        y = np.array(self.history)

        model = LinearRegression().fit(X, y)

        future_X = np.arange(len(self.history), len(self.history)+steps).reshape(-1,1)
        pred = model.predict(future_X)

        return pred.tolist()

forecaster_phi = Forecaster()
forecaster_H = Forecaster()
forecaster_I = Forecaster()
