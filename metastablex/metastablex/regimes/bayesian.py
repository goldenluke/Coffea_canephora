import numpy as np

class BayesianFilter:
    def __init__(self, n_states):
        self.belief = np.ones(n_states) / n_states

    def update(self, likelihood):
        posterior = likelihood * self.belief
        self.belief = posterior / np.sum(posterior)
        return self.belief
