import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.ndimage import gaussian_filter1d

import os
os.makedirs("plots", exist_ok=True)

# =========================
# FASTA
# =========================
def load_fasta(path, max_len=8_000_000):
    seq = ""
    with open(path) as f:
        for line in f:
            if not line.startswith(">"):
                seq += line.strip().upper()
                if len(seq) >= max_len:
                    break
    return seq

# =========================
# FEATURES
# =========================
def entropy(seq):
    counts = Counter(seq)
    probs = [v/len(seq) for v in counts.values()]
    return -sum(p*np.log2(p+1e-9) for p in probs)

def gc(seq):
    return (seq.count("G")+seq.count("C"))/len(seq)

def complexity(seq):
    return len(set(seq))/len(seq)

def extract(seq, window):
    feats = []
    for i in range(0, len(seq)-window, window):
        w = seq[i:i+window]
        feats.append([gc(w), entropy(w), complexity(w)])
    return np.array(feats)

# =========================
# PIPELINE
# =========================
def run_pipeline(seq, window=1500):

    X = extract(seq, window)
    X_scaled = StandardScaler().fit_transform(X)

    P = PCA(n_components=2).fit_transform(X_scaled)

    signal = P[:,0]

    smooth = gaussian_filter1d(signal, sigma=20)
    smooth = (smooth - smooth.min())/(smooth.max()-smooth.min())

    risk = np.abs(np.gradient(smooth))
    risk = gaussian_filter1d(risk, sigma=6)
    risk = risk / np.max(risk)

    return X, P, smooth, risk

# =========================
# LOAD
# =========================
print("🧬 loading genome...")
seq = load_fasta("data/arabidopsis.fa")

# =========================
# REAL
# =========================
print("⚙ running real...")
X, P, real_s, real_r = run_pipeline(seq)

# =========================
# SHUFFLE
# =========================
print("🎲 shuffle...")
seq_list = list(seq)
np.random.shuffle(seq_list)
seq_shuf = "".join(seq_list)

_, _, shuf_s, shuf_r = run_pipeline(seq_shuf)

# =========================
# AUTOCORR
# =========================
def autocorr(x):
    return np.correlate(x, x, mode='full')[len(x)-1:]

ac_real = autocorr(real_r)[:800]
ac_shuf = autocorr(shuf_r)[:800]

# =========================
# DELTA
# =========================
delta = real_r - shuf_r

# =========================
# FIGURA FINAL
# =========================
plt.figure(figsize=(12,14))

# A — PCA
ax1 = plt.subplot(5,1,1)
sc = ax1.scatter(P[:,0], P[:,1], c=P[:,0], s=5)
ax1.set_title("A) Structural Manifold", fontweight="bold")
ax1.set_xticks([])
ax1.set_yticks([])
plt.colorbar(sc, ax=ax1, label="PC1")

# B — STRUCTURE
ax2 = plt.subplot(5,1,2)
ax2.plot(real_s)
ax2.set_title("B) Structural Axis", fontweight="bold")

# C — RISK
ax3 = plt.subplot(5,1,3)
ax3.plot(real_r, label="Real")
ax3.plot(shuf_r, label="Shuffle", alpha=0.6)
ax3.legend(frameon=False)
ax3.set_title("C) Metastable Risk", fontweight="bold")

# D — DISTRIBUTION
ax4 = plt.subplot(5,1,4)
sns.kdeplot(real_r, label="Real", fill=True, alpha=0.4)
sns.kdeplot(shuf_r, label="Shuffle", fill=True, alpha=0.3)
ax4.legend(frameon=False)
ax4.set_title("D) Risk Distribution", fontweight="bold")

# E — DELTA + AUTOCORR 🔥
ax5 = plt.subplot(5,1,5)
ax5.plot(delta[:2000], label="Delta (Real-Shuffle)", alpha=0.7)
ax5.plot(ac_real[:500]/np.max(ac_real), label="Autocorr Real")
ax5.plot(ac_shuf[:500]/np.max(ac_shuf), label="Autocorr Shuffle")
ax5.legend(frameon=False)
ax5.set_title("E) Structural Difference & Memory", fontweight="bold")

plt.tight_layout()
plt.savefig("plots/figure_nature_final.png", dpi=300)
plt.savefig("plots/figure_nature_final.pdf")

print("🔥 UPDATED FIGURE SAVED → plots/figure_nature_final")

