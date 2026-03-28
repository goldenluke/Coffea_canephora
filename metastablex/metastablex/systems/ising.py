import numpy as np
from .base import ComplexSystem

class IsingModel(ComplexSystem):

    def __init__(self, size=30, temperature=2.2, steps=1000):
        super().__init__(steps)
        self.size = size
        self.temperature = temperature
        self.grid = np.random.choice([-1,1], (size,size))

    def step(self):

        i = np.random.randint(0,self.size)
        j = np.random.randint(0,self.size)

        spin = self.grid[i,j]

        neighbors = (
            self.grid[(i+1)%self.size,j] +
            self.grid[(i-1)%self.size,j] +
            self.grid[i,(j+1)%self.size] +
            self.grid[i,(j-1)%self.size]
        )

        dE = 2 * spin * neighbors

        if dE < 0 or np.random.rand() < np.exp(-dE/self.temperature):
            self.grid[i,j] *= -1

    def magnetization(self):
        return np.mean(self.grid)

    def simulate(self):

        m = []

        for _ in range(self.n_steps):
            self.step()
            m.append(self.magnetization())

        return np.array(m)
