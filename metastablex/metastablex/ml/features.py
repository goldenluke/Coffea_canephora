import torch


def metastable_features(x):

    # =========================
    # GARANTIR 1D
    # =========================
    x = torch.tensor(x, dtype=torch.float32)

    # 🔥 CORREÇÃO CRÍTICA
    if x.ndim > 1:
        x = x.flatten()

    N = len(x)

    # =========================
    # VARIÂNCIA
    # =========================
    mean = torch.mean(x)
    var = (x - mean) ** 2

    # =========================
    # AUTOCORRELAÇÃO
    # =========================
    ac = torch.zeros(N)

    if N > 1:
        ac[1:] = x[1:] * x[:-1]

    # =========================
    # ENTROPIA LOCAL
    # =========================
    ent = torch.zeros(N)

    window = 5

    for i in range(N):

        start = max(0, i - window)
        segment = x[start:i+1]

        if len(segment) < 2:
            continue

        p = torch.abs(segment) + 1e-8
        p = p / torch.sum(p)

        ent[i] = -torch.sum(p * torch.log(p))

    # =========================
    # STACK
    # =========================
    features = torch.stack([var, ac, ent], dim=1)

    return features
