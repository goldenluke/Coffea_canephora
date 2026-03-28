import numpy as np

class RegimeDetector:

    def __init__(self):
        self.history = []

    def detect(self, Phi, I):

        self.history.append(Phi)
        if len(self.history) > 20:
            self.history.pop(0)

        # ainda aquecendo
        if len(self.history) < 10:
            return "warming"

        recent = np.array(self.history)

        # 🔥 variação temporal
        dPhi = np.mean(np.abs(np.diff(recent)))

        # 🧠 REGRAS MELHORES

        # 🟢 STABLE: baixa variância + pouca mudança
        if I < 0.3 and dPhi < 0.01:
            return "stable"

        # 🔴 CHAOTIC: alta variância OU alta variação temporal
        if I > 1.0 or dPhi > 0.08:
            return "chaotic"

        # 🟡 CRITICAL: transição intermediária
        return "critical"
