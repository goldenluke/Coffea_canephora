import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats, signal
import math
import warnings
import os

warnings.filterwarnings("ignore")

st.set_page_config(page_title="QWAN Cardiology Complexity Lab", layout="wide")

os.makedirs("plots", exist_ok=True)


# ============================================================
# HRV SIMULATION
# ============================================================

def simulate_hrv(n=1500, regime="healthy", seed=42):

    np.random.seed(seed)

    hr = np.zeros(n)
    hr[0] = 70

    sympathetic = 0
    parasympathetic = 0

    for t in range(1, n):

        sympathetic = 0.95 * sympathetic + np.random.normal(0, 0.5)
        parasympathetic = 0.95 * parasympathetic + np.random.normal(0, 0.5)

        balance = sympathetic - parasympathetic

        if regime == "healthy":
            alpha = 0.6
            beta = 0.4
            noise = 0.05

        elif regime == "rigid":
            alpha = 0.9
            beta = 0.05
            noise = 0.005

        elif regime == "chaotic":
            alpha = 0.2
            beta = 0.8
            noise = 0.2

        else:
            alpha = 0.6
            beta = 0.4
            noise = 0.05

        dhr = (
            -alpha * (hr[t-1] - 70)
            + beta * balance
            + noise * np.random.randn()
        )

        hr[t] = hr[t-1] + dhr

    rr = 60 / hr

    return rr


# ============================================================
# COMPLEXITY ENGINE
# ============================================================

class UltraHealthEngine:

    def __init__(self, series):

        self.series = np.array(series)
        self.returns = np.diff(self.series) / np.mean(self.series)

    def dfa_alpha(self, ts):

        y = np.cumsum(ts - np.mean(ts))
        n_vals = np.unique(np.logspace(1, 2, 8).astype(int))

        rms_vals = []

        for n in n_vals:

            segments = len(y) // n

            if segments == 0:
                continue

            rms = np.sqrt(np.mean([
                np.mean((y[i*n:(i+1)*n] -
                np.polyval(np.polyfit(np.arange(n), y[i*n:(i+1)*n], 1), np.arange(n)))**2)
                for i in range(segments)
            ]))

            rms_vals.append(rms)

        if len(rms_vals) < 2:
            return 0.5

        return np.polyfit(np.log(n_vals[:len(rms_vals)]), np.log(rms_vals), 1)[0]

    def lempel_ziv(self, ts):

        s = "".join(['1' if x > np.median(ts) else '0' for x in ts])

        n = len(s)

        i, u, v, w, c = 1, 1, 1, 1, 1

        while v + w <= n:

            if s[i:i+v] == s[i+w:i+v+w]:
                v += 1
            else:
                w += 1
                c += 1
                v = 1

        return (c * math.log2(n)) / n

    def fisher_info(self, ts):

        h, _ = np.histogram(ts, bins=20, density=True)

        prob = h / (np.sum(h) + 1e-12)

        return 4 * np.sum(np.diff(np.sqrt(prob))**2)

    def permutation_entropy(self, ts, d=3):

        patterns = [tuple(np.argsort(ts[i:i+d])) for i in range(len(ts)-d+1)]

        _, counts = np.unique(patterns, axis=0, return_counts=True)

        p = counts / counts.sum()

        return -np.sum(p * np.log2(p)) / np.log2(math.factorial(d))

    def reconstruct_potential(self):

        hist, bins = np.histogram(self.returns, bins=30, density=True)

        centers = (bins[:-1] + bins[1:]) / 2

        sigma = np.std(self.returns)

        p = hist + 1e-12

        U = - (sigma**2 / 2) * np.log(p)

        return centers, U

    def multiscale_entropy(self, max_scale=10):

        ts = self.returns
        entropies = []

        for scale in range(1, max_scale + 1):

            if len(ts) // scale < 3:
                entropies.append(np.nan)
                continue

            rescaled = ts[:len(ts)-len(ts)%scale].reshape(-1, scale).mean(axis=1)

            entropies.append(self.permutation_entropy(rescaled))

        return np.array(entropies)


# ============================================================
# STREAMLIT UI
# ============================================================

st.title("Cardiology Complexity Dashboard")

st.sidebar.header("Simulation")

regime = st.sidebar.selectbox(
    "Cardiac Regime",
    ["healthy", "rigid", "chaotic"]
)

nbeats = st.sidebar.slider(
    "Number of beats",
    500,
    3000,
    1500
)

if st.sidebar.button("Run Simulation"):

    rr = simulate_hrv(nbeats, regime)

    ts = pd.Series(rr)

    engine = UltraHealthEngine(ts)

    alpha = engine.dfa_alpha(engine.returns)
    lz = engine.lempel_ziv(engine.returns)
    fisher = engine.fisher_info(engine.returns)

    hr = 60 / rr

    mean_hr = np.mean(hr)
    sdnn = np.std(rr, ddof=1)
    rmssd = np.sqrt(np.mean(np.diff(rr)**2))

    st.header("Clinical Metrics")

    c1, c2, c3, c4 = st.columns(4)

    c1.metric("Mean HR", f"{mean_hr:.1f} bpm")
    c2.metric("SDNN", f"{sdnn:.4f}")
    c3.metric("RMSSD", f"{rmssd:.4f}")
    c4.metric("Fractal Alpha", f"{alpha:.3f}")

    st.divider()

    plt.style.use("dark_background")

    fig = plt.figure(figsize=(20, 24))
    gs = gridspec.GridSpec(5, 2, figure=fig)

    ax1 = fig.add_subplot(gs[0, :])
    ax1.plot(hr, color="cyan")
    ax1.set_title("Heart Rate")
    ax1.grid(alpha=0.2)

    ax2 = fig.add_subplot(gs[1, 0])
    ax2.plot(rr)
    ax2.set_title("RR Intervals")
    ax2.grid(alpha=0.2)

    ax3 = fig.add_subplot(gs[1, 1])
    ax3.hist(engine.returns, bins=30)
    ax3.set_title("Return Distribution")

    ax4 = fig.add_subplot(gs[2, 0])
    centers, U = engine.reconstruct_potential()
    ax4.plot(centers, U)
    ax4.set_title("Potential Landscape")

    ax5 = fig.add_subplot(gs[2, 1])
    ax5.scatter(rr[:-1], rr[1:], alpha=0.4)
    ax5.set_title("Phase Space")

    ax6 = fig.add_subplot(gs[3, 0])
    f, pxx = signal.welch(engine.returns, fs=4.0)
    ax6.semilogy(f, pxx)
    ax6.set_title("Power Spectrum")

    ax7 = fig.add_subplot(gs[3, 1])
    mse = engine.multiscale_entropy()
    ax7.plot(range(1,11), mse)
    ax7.set_title("Multiscale Entropy")

    ax8 = fig.add_subplot(gs[4, :])
    ax8.axis("off")

    if sdnn < 0.02:
        status = "LOW HRV — possible pathological rigidity"
    elif 0.02 <= sdnn <= 0.08:
        status = "NORMAL PHYSIOLOGICAL VARIABILITY"
    else:
        status = "HIGH INSTABILITY — possible arrhythmia"

    text = f"""
Cardiac Regime: {regime}

Mean HR: {mean_hr:.1f} bpm
SDNN: {sdnn:.4f}
RMSSD: {rmssd:.4f}

Fractal Alpha: {alpha:.3f}
Fisher Information: {fisher:.2f}
Lempel-Ziv Complexity: {lz:.2f}

Interpretation:
{status}
"""

    ax8.text(
        0.05,
        0.5,
        text,
        fontsize=16,
        family="monospace"
    )

    plt.tight_layout()

    st.pyplot(fig)

else:

    st.info("Configure parameters and run simulation.")
