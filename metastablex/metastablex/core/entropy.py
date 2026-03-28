import numpy as np
import pandas as pd


def entropia_rolling(serie, window=3):

    serie = pd.Series(serie).fillna(0)

    if len(serie) < window:
        return pd.Series([0]*len(serie))

    out = []

    for i in range(len(serie)):
        if i < window:
            out.append(0)
            continue

        w = serie[i-window:i]
        hist, _ = np.histogram(w, bins=5, density=True)
        hist = hist + 1e-9

        ent = -np.sum(hist * np.log(hist))
        out.append(ent)

    return pd.Series(out)
