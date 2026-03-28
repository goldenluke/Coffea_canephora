import torch
import torch.nn as nn

class NeuralOperator(nn.Module):
    def __init__(self, dim=1):
        super().__init__()

        self.net = nn.Sequential(
            nn.Linear(1, 32),
            nn.ReLU(),
            nn.Linear(32, 32),
            nn.ReLU(),
            nn.Linear(32, 1)
        )

    def forward(self, x):
        x_in = x.unsqueeze(-1)  # (N) → (N,1)
        out = self.net(x_in)
        return out.squeeze(-1)
