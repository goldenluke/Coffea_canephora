import numpy as np

def compute_scale_metrics(series):

    returns = np.diff(series)

    variance = np.var(returns)

    if len(returns) > 2:
        ac1 = np.corrcoef(returns[:-1], returns[1:])[0,1]
    else:
        ac1 = 0

    hist,_ = np.histogram(returns,bins=20,density=True)
    p = hist + 1e-12

    entropy = -np.sum(p*np.log(p))

    complexity = entropy

    stability = 1/(1+variance+abs(ac1))

    energy = np.mean(series**2)

    return complexity, stability, energy
