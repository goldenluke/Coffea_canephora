import torch
import torch.nn as nn

class NeuralOperator(nn.Module):
    def __init__(self, hidden=64):
        super().__init__()

        self.net = nn.Sequential(
            nn.Conv1d(1, hidden, 3, padding=1),
            nn.ReLU(),
            nn.Conv1d(hidden, hidden, 3, padding=1),
            nn.ReLU(),
            nn.Conv1d(hidden, 1, 3, padding=1)
        )

    def forward(self, x):
        # x: (batch, 1, T)
        return self.net(x).mean()
