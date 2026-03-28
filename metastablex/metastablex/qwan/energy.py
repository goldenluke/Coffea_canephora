import torch

# =========================
# ENTROPIA
# =========================
def entropy(x):
    if x.dim() == 1:
        x_norm = (x - x.min()) / (x.max() - x.min() + 1e-8)
        p = x_norm / (x_norm.sum() + 1e-8)
        return -torch.sum(p * torch.log(p + 1e-8))

    elif x.dim() == 2:
        x_norm = (x - x.min(dim=1, keepdim=True)[0]) / (
            x.max(dim=1, keepdim=True)[0] - x.min(dim=1, keepdim=True)[0] + 1e-8
        )
        p = x_norm / (x_norm.sum(dim=1, keepdim=True) + 1e-8)
        return -torch.mean(torch.sum(p * torch.log(p + 1e-8), dim=1))


# =========================
# COERÊNCIA (simples)
# =========================
def coherence(x):
    # suporta batch (B, T)
    if x.dim() == 1:
        if len(x) < 2:
            return torch.tensor(0.0, requires_grad=True)
        return torch.mean(x[1:] * x[:-1])

    elif x.dim() == 2:
        return torch.mean(x[:, 1:] * x[:, :-1])

# =========================
# ENERGIA LIVRE (proxy)
# =========================
def energy_free(x):
    if x.dim() == 1:
        return torch.var(x)
    elif x.dim() == 2:
        return torch.mean(torch.var(x, dim=1))


# =========================
# FUNCIONAL Φ
# =========================
def structural_energy(x, alpha=1.0, beta=1.0):
    H = entropy(x)
    I = coherence(x)
    E = energy_free(x)

    return E - alpha * H - beta * I
