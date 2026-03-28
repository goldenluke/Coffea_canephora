import numpy as np
from hmmlearn.hmm import GaussianHMM


def fit_hmm(serie, n_states=3):

    if hasattr(serie, "values"):
        serie = serie.values

    serie = np.array(serie)
    serie = np.nan_to_num(serie)

    if len(serie) < 5 or np.std(serie) < 1e-6:
        return np.zeros(len(serie))

    serie = (serie - np.mean(serie)) / (np.std(serie) + 1e-6)
    serie = serie.reshape(-1, 1)

    model = GaussianHMM(n_components=n_states, n_iter=200)
    model.fit(serie)

    return model.predict(serie)
