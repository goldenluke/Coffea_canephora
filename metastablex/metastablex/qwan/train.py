import torch
import torch.nn as nn
import torch.optim as optim

from .neural_operator import NeuralOperator
from .batch_engine import evolve_batch

def train_model(df, municipios, epochs=50, device="cuda"):

    model = NeuralOperator().to(device)
    optimizer = optim.Adam(model.parameters(), lr=1e-3)

    for epoch in range(epochs):

        batch = build_batch(df, municipios, device=device)

        x_final, _ = evolve_batch(batch, model)

        # target: queremos estabilidade → minimizar variância final
        loss = torch.var(x_final)

        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

        print(f"Epoch {epoch} | Loss: {loss.item():.4f}")

    return model
