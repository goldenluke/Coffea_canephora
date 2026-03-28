import torch.nn.functional as F

def regime_loss(pred_risk, true_events):

    # true_events = 1 (colapso), 0 (normal)
    return F.binary_cross_entropy(pred_risk, true_events)

def hybrid_loss(x_final, risk, target):

    stability_loss = torch.var(x_final)

    regime_loss_val = F.mse_loss(risk, target)

    return stability_loss + regime_loss_val
