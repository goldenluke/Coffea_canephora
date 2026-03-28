def predict(model, x):
    feats = metastable_features(x.unsqueeze(0))
    feats = feats.unsqueeze(1)

    y_pred, regimes, z = model(feats)

    return {
        "prediction": y_pred.item(),
        "regime_probs": regimes.detach().numpy(),
        "instability": torch.var(z).item()
    }
