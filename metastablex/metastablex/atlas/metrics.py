import numpy as np
from metastablex.physics.lyapunov import lyapunov_exponent

def compute_metrics(series):

    ts = np.array(series)

    returns = np.diff(ts)

    variance = np.var(returns)

    lyap = lyapunov_exponent(returns)

    entropy = -np.sum(
        np.histogram(returns,bins=20,density=True)[0]
    )

    complexity = entropy

    stability = 1/(1+variance+abs(lyap))

    return complexity, stability
