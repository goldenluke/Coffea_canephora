import numpy as np

class RegimeAlert:

    def __init__(self):
        self.prev_regime = None
        self.history = []

    def classify(self, lyap, shannon, perm):

        if lyap is None:
            return "warming"

        if lyap < -0.01:
            return "stable"

        if lyap > 0.03 or (perm and perm > 1.5):
            return "chaotic"

        return "critical"

    def update(self, lyap, shannon, perm):

        regime = self.classify(lyap, shannon, perm)

        alert = None

        if self.prev_regime and regime != self.prev_regime:
            alert = {
                "from": self.prev_regime,
                "to": regime,
                "type": f"{self.prev_regime}_to_{regime}"
            }

        self.prev_regime = regime

        return regime, alert
