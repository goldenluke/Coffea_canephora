import torch

class Environment:
    def __init__(self, size, mode="data", data=None):
        self.size = size
        self.mode = mode
        self.data = data

    def generate(self, t):
        if self.mode == "data" and self.data is not None:
            return self.data[t % len(self.data)]

        elif self.mode == "constant":
            return torch.ones(self.size) * 0.5

        elif self.mode == "shock":
            E = torch.zeros(self.size)
            if t > 50:
                E += 1.0
            return E

        elif self.mode == "noise":
            return torch.randn(self.size) * 0.2

        return torch.zeros(self.size)
