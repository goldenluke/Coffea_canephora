import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.ndimage import gaussian_filter1d

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
    X = StandardScaler().fit_transform(X)

    pca = PCA(n_components=2)
    P = pca.fit_transform(X)

    signal = P[:,0]

    smooth = gaussian_filter1d(signal, sigma=20)
    smooth = (smooth - smooth.min())/(smooth.max()-smooth.min())

    risk = np.abs(np.gradient(smooth))
    risk = gaussian_filter1d(risk, sigma=6)
    risk = risk / np.max(risk)

    return P, smooth, risk

# =========================
# LOAD
# =========================
print("🧬 loading genome...")
seq = load_fasta("data/arabidopsis.fa")

# =========================
# REAL
# =========================
print("⚙ running real...")
P, real_s, real_r = run_pipeline(seq)

# =========================
# SHUFFLE
# =========================
print("🎲 shuffle control...")
seq_list = list(seq)
np.random.shuffle(seq_list)
seq_shuf = "".join(seq_list)

_, shuf_s, shuf_r = run_pipeline(seq_shuf)

# =========================
# FIGURE (NATURE STYLE)
# =========================
print("📊 plotting...")

plt.figure(figsize=(10,10))

# A — PCA
ax1 = plt.subplot(4,1,1)
sc = ax1.scatter(P[:,0], P[:,1], c=P[:,0], s=6)
ax1.set_title("A) Structural Manifold", fontweight="bold")
ax1.set_xticks([])
ax1.set_yticks([])
plt.colorbar(sc, ax=ax1, label="PC1")

# B — STRUCTURE
ax2 = plt.subplot(4,1,2)
ax2.plot(real_s, linewidth=1)
ax2.set_title("B) Structural Axis", fontweight="bold")

# C — RISK
ax3 = plt.subplot(4,1,3)
ax3.plot(real_r, label="Real", linewidth=1.2)
ax3.plot(shuf_r, label="Shuffled", alpha=0.6)
ax3.legend(frameon=False)
ax3.set_title("C) Metastable Risk", fontweight="bold")

# D — DISTRIBUTION (KDE)
ax4 = plt.subplot(4,1,4)
sns.kdeplot(real_r, label="Real", fill=True, alpha=0.4)
sns.kdeplot(shuf_r, label="Shuffled", fill=True, alpha=0.3)
ax4.legend(frameon=False)
ax4.set_title("D) Risk Distribution", fontweight="bold")

plt.tight_layout()

import os
os.makedirs("plots", exist_ok=True)

plt.savefig("plots/figure_nature_final.png", dpi=300)
plt.savefig("plots/figure_nature_final.pdf")

# =========================
# STATS
# =========================
print("\n📊 COMPARISON")
print("Real mean:", np.mean(real_r))
print("Shuffle mean:", np.mean(shuf_r))
print("Effect size:", np.mean(real_r) - np.mean(shuf_r))

print("\n🔥 DONE")
print("📁 saved in plots/")

