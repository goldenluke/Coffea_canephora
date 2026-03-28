import numpy as np
import torch

from .ml.train import train
from .ml.features import metastable_features


class MetastableModel:

    def __init__(self):
        self.model = None

    def fit(self, series):
        series = np.array(series, dtype=float)
        self.model = train(series)
        return self

    def predict(self, series):
        if self.model is None:
            raise ValueError("Model not trained")

        series = np.array(series, dtype=float)
        feats = metastable_features(series)

        with torch.no_grad():
            preds = self.model(feats).numpy()

        return float(preds.mean())

    def classify(self, score):
        if score > 0.66:
            return "critical"
        elif score > 0.5:
            return "metastable"
        else:
            return "stable"
