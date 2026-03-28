import numpy as np
from metastablex.physics.lyapunov import lyapunov_exponent
from metastablex.core.potential import potential_landscape

def compute_3d_metrics(series):

    ts = np.array(series)
    returns = np.diff(ts)

    variance = np.var(returns)

    ac1 = np.corrcoef(returns[:-1], returns[1:])[0,1]

    lyap = lyapunov_exponent(returns)

    # complexity proxy
    hist,_ = np.histogram(returns,bins=20,density=True)
    p = hist + 1e-12
    entropy = -np.sum(p*np.log(p))

    complexity = entropy

    stability = 1/(1+variance+abs(lyap)+abs(ac1))

    centers,U = potential_landscape(returns)

    energy = np.mean(U)

    return complexity, stability, energy
