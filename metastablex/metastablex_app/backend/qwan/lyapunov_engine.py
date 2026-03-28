import torch
import numpy as np

class LyapunovCalculator:

    def __init__(self, eps=1e-5):
        self.eps = eps
        self.initialized = False
        self.sum_log = 0.0
        self.steps = 0

    def init(self, field):
        self.ref = field.clone()
        self.pert = field.clone() + self.eps * torch.randn_like(field)
        self.initialized = True
        self.sum_log = 0.0
        self.steps = 0

    def step(self, evolve_fn):

        if not self.initialized:
            return None

        # evolui os dois sistemas
        self.ref = evolve_fn(self.ref)
        self.pert = evolve_fn(self.pert)

        d = torch.norm(self.pert - self.ref)

        if d.item() == 0:
            return None

        # 🔥 incremento logarítmico
        log_term = torch.log(d / self.eps).item()

        self.sum_log += log_term
        self.steps += 1

        # 🔁 renormalização
        direction = (self.pert - self.ref) / d
        self.pert = self.ref + self.eps * direction

        # 🔥 MÉDIA (ESSENCIAL)
        lyap = self.sum_log / self.steps

        return lyap
