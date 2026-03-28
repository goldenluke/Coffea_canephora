import torch

def alignment(x, E):
    return torch.corrcoef(torch.stack([x, E]))[0,1].item()

def classify_regime(H, I):
    if H > I * 1.5:
        return "CHAOTIC"
    elif I > H * 1.5:
        return "RIGID"
    else:
        return "METASTABLE"

def risk_score(H, I):
    return H / (I + 1e-6)
