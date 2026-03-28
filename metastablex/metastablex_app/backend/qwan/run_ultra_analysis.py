import numpy as np

from multifractal import mfdfa
from multifractal_plot import plot_multifractal
from ks_entropy import ks_entropy

# exemplo (substituir por Phi real depois)
series = np.random.randn(1000)

# =========================
# MULTIFRACTAL
# =========================
alpha, f_alpha = mfdfa(series)
plot_multifractal(alpha, f_alpha)

# =========================
# KS ENTROPY (exemplo)
# =========================
lyap = [0.12, 0.03, -0.4]
ks = ks_entropy(lyap)

print("KS Entropy:", ks)

print("DONE")
