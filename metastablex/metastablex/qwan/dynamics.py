import torch
from .gradients import compute_gradients

def evolve(
    x,
    model=None,
    steps=50,
    dt=0.01,
    alpha=1.0,
    beta=1.0,
    k=0.1,
    sigma=0.01,
    device="cpu"
):
    x = x.to(device)

    history = []

    for _ in range(steps):

        grad_E, grad_H, grad_I = compute_gradients(x, alpha, beta)

        # ambiente
        E_env = torch.mean(x)
        env = k * (E_env - x)

        # ruído
        noise = sigma * torch.randn_like(x)

        # operador neural
        if model is not None:
            neural = model(x)
        else:
            neural = torch.zeros_like(x)

        dx = (
            -grad_E
            + alpha * grad_H
            + beta * grad_I
            + env
            + noise
            + neural
        )

        x = x + dt * dx

        # métricas
        H = torch.mean(x).item()
        I = torch.var(x).item()
        Phi = torch.mean(dx).item()

        history.append({
            "H": H,
            "I": I,
            "Phi": Phi
        })

    return x.detach(), history
