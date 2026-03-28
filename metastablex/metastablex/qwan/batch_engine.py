import torch
from .gradients import compute_gradients

def evolve_batch(x, model, steps=50, dt=0.01, k=0.1, sigma=0.01):

    history = []

    for _ in range(steps):

        grad_E, grad_H, grad_I = compute_gradients(x)

        env = k * (x.mean(dim=1, keepdim=True) - x)

        noise = sigma * torch.randn_like(x)

        if model is not None:
            neural = model(x)
        else:
            neural = torch.zeros_like(x)

        dx = -grad_E + grad_H + grad_I + env + noise + neural

        x = x + dt * dx

        history.append(x.mean().item())

    return x, history
