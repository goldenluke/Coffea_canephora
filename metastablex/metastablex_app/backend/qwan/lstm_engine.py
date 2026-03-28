import torch
import torch.nn as nn

class LSTMModel(nn.Module):
    def __init__(self):
        super().__init__()
        self.lstm = nn.LSTM(1, 32, batch_first=True)
        self.fc = nn.Linear(32, 1)

    def forward(self, x):
        out, _ = self.lstm(x)
        return self.fc(out[:, -1, :])

class LSTMForecaster:
    def __init__(self):
        self.model = LSTMModel()
        self.data = []

    def update(self, value):
        self.data.append(value)
        if len(self.data) > 50:
            self.data.pop(0)

    def train(self):
        if len(self.data) < 10:
            return

        x = torch.tensor(self.data[:-1]).float().view(1, -1, 1)
        y = torch.tensor(self.data[1:]).float().view(1, -1, 1)

        optimizer = torch.optim.Adam(self.model.parameters(), lr=0.01)
        loss_fn = nn.MSELoss()

        for _ in range(5):
            pred = self.model(x)
            loss = loss_fn(pred, y[:, -1])
            optimizer.zero_grad()
            loss.backward()
            optimizer.step()

    def predict(self):
        if len(self.data) < 10:
            return None

        x = torch.tensor(self.data).float().view(1, -1, 1)
        return self.model(x).item()

lstm_phi = LSTMForecaster()
