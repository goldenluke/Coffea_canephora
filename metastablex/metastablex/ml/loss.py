import torch.nn.functional as F

def metastable_loss(y_pred, y_true, z=None, regimes=None):

    # 🔥 alinhar tamanhos
    min_len = min(len(y_pred), len(y_true))

    y_pred = y_pred[:min_len]
    y_true = y_true[:min_len]

    loss = F.mse_loss(y_pred.squeeze(), y_true)

    return loss, {"mse": loss.item()}
