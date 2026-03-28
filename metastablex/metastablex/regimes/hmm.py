from hmmlearn.hmm import GaussianHMM

class RegimeHMM:
    def __init__(self, n_states=3):
        self.model = GaussianHMM(n_components=n_states, covariance_type="full")

    def fit(self, X):
        self.model.fit(X)

    def predict(self, X):
        return self.model.predict(X)

    def probabilities(self, X):
        return self.model.predict_proba(X)
