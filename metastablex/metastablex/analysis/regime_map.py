import numpy as np

def complexity_index(lz, entropy, fisher):

    return np.mean([lz, entropy, fisher])


def stability_index(ac1, variance, lyapunov):

    ac1_norm = (ac1 + 1) / 2
    var_norm = variance / (variance + 1)

    return 1 - np.mean([ac1_norm, var_norm, abs(lyapunov)])


def regime_coordinates(metrics):

    C = complexity_index(
        metrics["lz"],
        metrics["entropy"],
        metrics["fisher"]
    )

    S = stability_index(
        metrics["ac1"],
        metrics["variance"],
        metrics["lyapunov"]
    )

    return C, S
