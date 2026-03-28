import torch
import torch.nn as nn

class MetastableXModel(nn.Module):
    def __init__(self, input_dim=3, hidden_dim=64, regimes=3):
        super().__init__()

        # embedding
        self.encoder = nn.Sequential(
            nn.Linear(input_dim, hidden_dim),
            nn.ReLU(),
            nn.Linear(hidden_dim, hidden_dim)
        )

        # dinâmica
        self.dynamics = nn.GRU(hidden_dim, hidden_dim, batch_first=True)

        # previsão
        self.predictor = nn.Linear(hidden_dim, 1)

        # regimes (soft)
        self.regime_head = nn.Linear(hidden_dim, regimes)

    def forward(self, x_feat):
        z = self.encoder(x_feat)

        out, _ = self.dynamics(z)

        last = out[:, -1]

        y_pred = self.predictor(last)
        regimes = torch.softmax(self.regime_head(last), dim=-1)

        return y_pred, regimes, z
