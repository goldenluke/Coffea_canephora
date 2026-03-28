import numpy as np

from takens import takens_embedding
from phase_reconstruction import plot_phase
from kaplan_yorke import kaplan_yorke_dimension

# fake exemplo (substituir por dados reais depois)
phi_series = np.random.randn(200)

# =========================
# TAKENS
# =========================
embedded = takens_embedding(phi_series, dim=3, tau=2)

# =========================
# PHASE
# =========================
plot_phase(embedded)

# =========================
# LYAPUNOV EXEMPLO
# =========================
lyap = [0.12, 0.01, -0.5]

D = kaplan_yorke_dimension(lyap)

print("Kaplan-Yorke dimension:", D)
print("DONE")
