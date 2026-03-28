import numpy as np
from scipy import stats

def compute_signature(ts):

    ts = np.array(ts)

    returns = np.diff(ts)

    variance = np.var(returns)

    ac1 = np.corrcoef(returns[:-1], returns[1:])[0,1]

    hist,_ = np.histogram(returns,bins=20,density=True)

    p = hist + 1e-12

    entropy = -np.sum(p*np.log(p))

    signature = {

        "variance": variance,
        "ac1": ac1,
        "entropy": entropy

    }

    return signature
