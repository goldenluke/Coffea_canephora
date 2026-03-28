import os
import numpy as np
import matplotlib.pyplot as plt
from tqdm import tqdm
from scipy.stats import gaussian_kde
from scipy import signal

# =========================
# CONFIG
# =========================
N = 300
STEPS = 200
OUT_DIR = "frames"
os.makedirs(OUT_DIR, exist_ok=True)

# =========================
# SIMULAÇÃO (BASEADA NO SEU PADRÃO HRV/QWAN)
# =========================
def simulate_series(n=300):
    x = np.zeros(n)
    x[0] = 0

    for t in range(1, n):
        noise = np.random.randn() * 0.05
        x[t] = 0.9 * x[t-1] + noise

    return x

# =========================
# DINÂMICA QWAN (COERENTE COM SUA ENGINE)
# =========================
def evolve_qwan(x, steps=100, k=0.3, sigma=0.02):
    history = []

    for t in range(steps):

        noise = sigma * np.random.randn(len(x))
        coupling = k * (np.mean(x) - x)

        dx = -0.1 * x + coupling + noise
        x = x + dx

        returns = np.diff(x + 1e-6)

        # ENTROPIA
        p = np.abs(returns) + 1e-8
        p = p / p.sum()
        H = -np.sum(p * np.log(p))

        # COERÊNCIA (inverso da variância)
        I = 1 / (np.var(returns) + 1e-6)

        # ENERGIA
        Phi = np.var(returns)

        history.append({
            "state": x.copy(),
            "returns": returns.copy(),
            "H": H,
            "I": I,
            "Phi": Phi
        })

    return history

# =========================
# INIT
# =========================
x0 = simulate_series(N)
history = evolve_qwan(x0, STEPS)

# =========================
# RENDER FRAMES (ESTILO SEU DASHBOARD)
# =========================
for i, h in enumerate(tqdm(history)):

    state = h["state"]
    returns = h["returns"]

    plt.figure(figsize=(12,8))

    # Série
    plt.subplot(3,2,1)
    plt.plot(state)
    plt.title(f"QWAN Field | step={i}")

    # Distribuição
    plt.subplot(3,2,2)
    plt.hist(returns, bins=30)
    plt.title("Distribution")

    # Potencial
    plt.subplot(3,2,3)
    kde = gaussian_kde(returns)
    x_vals = np.linspace(min(returns), max(returns), 200)
    p = kde(x_vals)
    U = -np.log(p + 1e-12)
    plt.plot(x_vals, U)
    plt.title("Potential")

    # Espectro
    plt.subplot(3,2,4)
    f, pxx = signal.welch(returns)
    plt.semilogy(f[1:], pxx[1:])
    plt.title("Power Spectrum")

    # Métricas QWAN
    plt.subplot(3,2,5)
    plt.bar(["H","I","Phi"], [h["H"], h["I"], h["Phi"]])
    plt.title("QWAN Metrics")

    plt.tight_layout()
    plt.savefig(f"{OUT_DIR}/frame_{i:04d}.png")
    plt.close()

print("Frames gerados.")
