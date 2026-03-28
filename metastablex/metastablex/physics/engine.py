import numpy as np

class MetastableXEngine:

    def __init__(
        self,
        potential,
        force=None,
        noise=0.05,
        dt=0.01,
        steps=2000
    ):

        self.potential = potential
        self.force = force if force else (lambda x,t: 0)

        self.noise = noise
        self.dt = dt
        self.steps = steps

    def gradU(self,x):

        eps = 1e-5
        return (self.potential(x+eps)-self.potential(x-eps))/(2*eps)

    def simulate(self,x0=0.1):

        x = np.zeros(self.steps)
        x[0] = x0

        for t in range(1,self.steps):

            drift = -self.gradU(x[t-1])
            forcing = self.force(x[t-1],t)

            noise_term = np.sqrt(2*self.noise)*np.random.randn()

            x[t] = (
                x[t-1]
                + (drift + forcing)*self.dt
                + noise_term*np.sqrt(self.dt)
            )

        return x
