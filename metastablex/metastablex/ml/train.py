import torch
import torch.nn as nn
import torch.optim as optim

from metastablex.ml.features import metastable_features
from metastablex.ml.loss import metastable_loss


class SimpleModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(3, 16),
            nn.ReLU(),
            nn.Linear(16, 1)
        )

    def forward(self, x):
        return self.net(x).squeeze()


def train(series):

    x = torch.tensor(series, dtype=torch.float32)

    feats = metastable_features(x)

    model = SimpleModel()

    optimizer = optim.Adam(model.parameters(), lr=0.01)

    for epoch in range(50):

        optimizer.zero_grad()

        y_pred = model(feats)

        # 🔥 alvo = série original
        y_true = x

        loss, _ = metastable_loss(y_pred, y_true)

        loss.backward()
        optimizer.step()

    return model
