import numpy as np


def detectar_ruptura(serie):

    serie = np.array(serie)

    if len(serie) < 5:
        return []

    dif = np.diff(serie)

    if np.std(dif) == 0:
        return []

    rupturas = np.where(np.abs(dif) > np.std(dif) * 2)[0]

    return rupturas.tolist()
