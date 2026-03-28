import numpy as np

from mutual_info import optimal_tau
from fnn import optimal_dimension
from takens import takens_embedding
from correlation_dimension import correlation_dimension

# exemplo (substituir por Phi real depois)
series = np.random.randn(500)

# =========================
# τ ótimo
# =========================
tau = optimal_tau(series)
print("Optimal tau:", tau)

# =========================
# dimensão ótima
# =========================
dim = optimal_dimension(series)
print("Optimal dimension:", dim)

# =========================
# embedding
# =========================
embedded = takens_embedding(series, dim=dim, tau=tau)

# =========================
# dimensão de correlação
# =========================
corr_dim = correlation_dimension(embedded)
print("Correlation dimension:", corr_dim)

print("DONE")
