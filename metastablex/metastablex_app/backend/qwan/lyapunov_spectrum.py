import torch
import numpy as np

class LyapunovSpectrum:

    def __init__(self, dim=3, eps=1e-6):
        self.dim = dim
        self.eps = eps
        self.initialized = False

    def init(self, field):
        self.ref = field.clone()

        self.vecs = []
        for _ in range(self.dim):
            v = torch.randn_like(field)
            v = v / torch.norm(v)
            self.vecs.append(v * self.eps)

        self.sums = [0.0]*self.dim
        self.steps = 0
        self.initialized = True

    def step(self, evolve_fn):

        if not self.initialized:
            return None

        self.ref = evolve_fn(self.ref)

        new_vecs = []

        for i, v in enumerate(self.vecs):

            pert = self.ref + v
            pert = evolve_fn(pert)

            diff = pert - self.ref
            norm = torch.norm(diff)

            if norm.item() == 0:
                continue

            self.sums[i] += torch.log(norm / self.eps).item()

            new_vecs.append(diff / norm * self.eps)

        self.vecs = new_vecs
        self.steps += 1

        return [s/self.steps for s in self.sums]
