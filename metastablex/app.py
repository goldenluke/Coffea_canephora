import streamlit as st
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from scipy import stats, signal
from scipy.stats import gaussian_kde
from pysus.online_data.SIH import SIH
import math
import warnings
import os
from metastablex.core.cardiology import simulate_hrv
# ============================================================
# PAGE CONFIGURATION
# ============================================================
st.set_page_config(page_title="QWAN Ultra-Deep Health Complexity", layout="wide")
warnings.filterwarnings("ignore")
os.makedirs("plots", exist_ok=True)

# ============================================================
# ULTRA HEALTH ENGINE
# ============================================================
class UltraHealthEngine:
    def __init__(self, series):
        self.series = np.array(series, dtype=float)
        self.returns = np.diff(np.log(self.series + 1e-6))

    def dfa_alpha(self, ts):
        if len(ts) < 20:
            return 0.5
        y = np.cumsum(ts - np.mean(ts))
        n_vals = np.unique(np.logspace(1, 2, 8).astype(int))
        rms_vals = []
        for n in n_vals:
            segments = len(y) // n
            if segments == 0:
                continue
            rms = np.sqrt(np.mean([
                np.mean(
                    (y[i*n:(i+1)*n] -
                     np.polyval(np.polyfit(np.arange(n), y[i*n:(i+1)*n], 1), np.arange(n)))**2
                )
                for i in range(segments)
            ]))
            rms_vals.append(rms)
        if len(rms_vals) < 2:
            return 0.5
        return np.polyfit(np.log(n_vals[:len(rms_vals)]), np.log(rms_vals), 1)[0]

    def lempel_ziv(self, ts):
        if len(ts) < 5:
            return 0
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
        if len(ts) < 10:
            return 0
        h, _ = np.histogram(ts, bins=20, density=True)
        prob = h / (np.sum(h) + 1e-12)
        return 4 * np.sum(np.diff(np.sqrt(prob))**2)

    def permutation_entropy(self, ts, d=3):
        ts_arr = np.array(ts)
        if len(ts_arr) < d:
            return 1.0
        patterns = [tuple(np.argsort(ts_arr[i:i+d])) for i in range(len(ts_arr)-d+1)]
        _, counts = np.unique(patterns, axis=0, return_counts=True)
        p = counts / counts.sum()
        return -np.sum(p * np.log2(p)) / np.log2(math.factorial(d))

    def multiscale_entropy(self, max_scale=10):
        ts = self.returns
        n = len(ts)
        entropies = []
        for scale in range(1, max_scale + 1):
            if n // scale < 5:
                entropies.append(1.0)
                continue
            rescaled = ts[:n - n % scale].reshape(-1, scale).mean(axis=1)
            entropies.append(self.permutation_entropy(rescaled))
        return np.array(entropies)

    def get_rolling_metrics(self, window=14):
        metrics = {
            'resilience': [], 'alpha': [], 'lz': [], 'fisher': [],
            'ac1': [], 'vol': [], 'skew': [], 'kurt': []
        }
        for i in range(window, len(self.returns)):
            slice_ts = self.returns[i-window:i]
            a = self.dfa_alpha(slice_ts)
            lz = self.lempel_ziv(slice_ts)
            f = self.fisher_info(slice_ts)
            ac1 = pd.Series(slice_ts).autocorr(lag=1)
            vol = np.std(slice_ts)
            ac1_norm = ((ac1 if not np.isnan(ac1) else 0) + 1) / 2
            risk = (ac1_norm + a + (np.log10(vol**2+1e-9)+4)/4) / 3
            metrics['resilience'].append(1 - risk)
            metrics['alpha'].append(a)
            metrics['lz'].append(lz)
            metrics['fisher'].append(f)
            metrics['ac1'].append(ac1)
            metrics['vol'].append(vol)
            metrics['skew'].append(stats.skew(slice_ts))
            metrics['kurt'].append(stats.kurtosis(slice_ts))
        return {k: np.array(v) for k, v in metrics.items()}

# ============================================================
# DATA PIPELINE
# ============================================================
@st.cache_data
@st.cache_data
def load_cardiology_data(regime, n=1500):
    rr = simulate_hrv(n=n, regime=regime)
    ts = pd.Series(rr)
    return ts

# ============================================================
# STREAMLIT UI
# ============================================================
st.title("🔬 QWAN Ultra-Deep Structural Monitoring")
st.markdown("Application of nonlinear dynamics and statistical physics to hospitalization data.")

st.sidebar.header("Control Panel")
with st.sidebar:
    uf = st.selectbox("State", ["SP", "RJ", "TO", "MG", "BA", "PR", "AM"])
    year = st.number_input("Year", 2015, 2024, 2023)
    month = st.slider("Month", 1, 12, 1)
    cid = st.text_input("ICD-10 Chapter", "J")
    agg = st.selectbox("Aggregation", ["D", "W"], format_func=lambda x: "Daily" if x=="D" else "Weekly")
    window = st.slider("Rolling Window", 7, 30, 14)
    theme = st.toggle("Dark Mode", True)

if st.sidebar.button("Run Diagnostic"):

    ts = load_data(uf, year, month, cid, agg)

    if ts.empty or len(ts) < window:
        st.warning("Insufficient data.")
    else:
        engine = UltraHealthEngine(ts)
        roll = engine.get_rolling_metrics(window)

        plt.style.use("dark_background" if theme else "default")
        fig = plt.figure(figsize=(24, 30))
        gs = gridspec.GridSpec(6, 3, figure=fig)

        # 1 Raw Series
        ax1 = fig.add_subplot(gs[0, :])
        ma = ts.rolling(7).mean()
        std = ts.rolling(7).std()
        ax1.plot(ts.values, lw=2)
        ax1.plot(ma.values, lw=2)
        ax1.fill_between(range(len(ts)),
                         (ma-std).values,
                         (ma+std).values,
                         alpha=0.2)
        ax1.set_title("Raw Time Series + Volatility Envelope")

        # 2 Resilience
        ax2 = fig.add_subplot(gs[1, :2])
        ax2.plot(roll['resilience'], lw=2)
        ax2.axhline(0.4, ls="--")
        ax2.set_title("Systemic Resilience")

        # 3 AC1
        ax3 = fig.add_subplot(gs[1, 2])
        ax3.plot(roll['ac1'], lw=2)
        ax3.set_title("Critical Slowing Down (AC1)")

        # 4 DFA
        ax4 = fig.add_subplot(gs[2, 0])
        ax4.plot(roll['alpha'])
        ax4.set_title("Fractal Memory (DFA)")

        # 5 Fisher
        ax5 = fig.add_subplot(gs[2, 1])
        ax5.plot(roll['fisher'])
        ax5.set_title("Fisher Information")

        # 6 LZ
        ax6 = fig.add_subplot(gs[2, 2])
        ax6.plot(roll['lz'])
        ax6.set_title("Lempel-Ziv Complexity")

        # 7 Potential
        ax7 = fig.add_subplot(gs[3, 0])
        kde = gaussian_kde(engine.returns)
        x_vals = np.linspace(min(engine.returns), max(engine.returns), 200)
        p = kde(x_vals)
        sigma = np.std(engine.returns)
        U = -(sigma**2 / 2) * np.log(p + 1e-12)
        ax7.plot(x_vals, U)
        ax7.set_title("Effective Potential")

        # 8 Power Spectrum
        ax8 = fig.add_subplot(gs[3, 1])
        f, pxx = signal.welch(engine.returns)
        ax8.loglog(f[1:], pxx[1:])
        ax8.set_title("Power Spectrum")

        # 9 Multiscale Entropy
        ax9 = fig.add_subplot(gs[3, 2])
        mse = engine.multiscale_entropy()
        ax9.plot(range(1,11), mse)
        ax9.set_title("Multiscale Entropy")

        plt.tight_layout()
        st.pyplot(fig)

else:
    st.info("Configure parameters and run the diagnostic.")
