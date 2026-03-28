import numpy as np
from metastablex.tensor.regime_tensor import build_regime_tensor

class RegimeRG:

    def __init__(self, scales):

        self.scales = scales

    def flow(self, ts):

        tensor = build_regime_tensor(ts, self.scales)

        C = tensor[:,0]
        S = tensor[:,1]
        E = tensor[:,2]
        T = tensor[:,3]

        flow = []

        for i in range(len(tensor)-1):

            dC = C[i+1] - C[i]
            dS = S[i+1] - S[i]
            dE = E[i+1] - E[i]

            flow.append([C[i],S[i],E[i],dC,dS,dE,T[i]])

        return np.array(flow)
