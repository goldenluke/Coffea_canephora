import numpy as np
from .base import ComplexSystem

class MarketModel(ComplexSystem):

    def __init__(self, steps=2000, volatility=0.02):

        super().__init__(steps)

        self.volatility = volatility

    def simulate(self):

        price = [100]

        for _ in range(self.n_steps):

            shock = np.random.randn()*self.volatility

            price.append(price[-1]*np.exp(shock))

        return np.array(price)
