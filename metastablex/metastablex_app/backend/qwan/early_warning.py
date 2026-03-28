import numpy as np

class EarlyWarning:

    def __init__(self):
        self.lyap_hist = []
        self.phi_hist = []
        self.perm_hist = []

    def update(self, lyap, phi, perm):

        if lyap is None:
            return None

        self.lyap_hist.append(lyap)
        self.phi_hist.append(phi)
        self.perm_hist.append(perm if perm else 0)

        # manter janela
        self.lyap_hist = self.lyap_hist[-30:]
        self.phi_hist = self.phi_hist[-30:]
        self.perm_hist = self.perm_hist[-30:]

        if len(self.lyap_hist) < 10:
            return None

        # =========================
        # SINAIS DE TRANSIÇÃO
        # =========================

        lyap_trend = np.polyfit(range(len(self.lyap_hist)), self.lyap_hist, 1)[0]
        phi_trend = np.polyfit(range(len(self.phi_hist)), self.phi_hist, 1)[0]
        perm_mean = np.mean(self.perm_hist)

        # 🔥 HEURÍSTICA FORTE

        if lyap_trend > 0.01 and phi_trend > 0:
            return {
                "type": "approaching_chaos",
                "strength": float(lyap_trend + phi_trend),
            }

        if lyap_trend < -0.01:
            return {
                "type": "stabilizing",
                "strength": float(abs(lyap_trend)),
            }

        if perm_mean > 1.2:
            return {
                "type": "high_complexity",
                "strength": float(perm_mean),
            }

        return None
