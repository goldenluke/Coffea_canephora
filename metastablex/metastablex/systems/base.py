import numpy as np

class ComplexSystem:

    def __init__(self, n_steps=1000, seed=None):

        self.n_steps = n_steps
        self.seed = seed

        if seed is not None:
            np.random.seed(seed)

    def simulate(self):
        raise NotImplementedError
