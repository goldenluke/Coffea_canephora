#!/usr/bin/env bash
set -e

echo "🔥 MetastableX FINAL (shuffle + nature figure)"

mkdir -p plots

cat << 'PYEOF' > final_analysis.py
import numpy as np
import pandas as pd
from collections import Counter
import matplotlib.pyplot as plt

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
# PIPELINE CORE
# =========================
def run_pipeline(seq, window=1500):

    X = extract(seq, window)
    X = StandardScaler().fit_transform(X)

    signal = PCA(n_components=1).fit_transform(X).flatten()

    smooth = gaussian_filter1d(signal, sigma=20)
    smooth = (smooth - smooth.min())/(smooth.max()-smooth.min())

    risk = np.abs(np.gradient(smooth))
    risk = gaussian_filter1d(risk, sigma=6)
    risk = risk / np.max(risk)

    return smooth, risk


# =========================
# LOAD REAL
# =========================
print("🧬 loading real genome...")
seq = load_fasta("data/arabidopsis.fa")

real_s, real_r = run_pipeline(seq)

# =========================
# SHUFFLE CONTROL
# =========================
print("🎲 generating shuffle control...")
seq_list = list(seq)
np.random.shuffle(seq_list)
seq_shuffled = "".join(seq_list)

shuf_s, shuf_r = run_pipeline(seq_shuffled)

# =========================
# PCA (real only)
# =========================
X = extract(seq, 1500)
X = StandardScaler().fit_transform(X)
P = PCA(n_components=2).fit_transform(X)

# =========================
# FIGURA FINAL (NATURE STYLE)
# =========================
fig = plt.figure(figsize=(12,10))

# A — MANIFOLD
ax1 = plt.subplot(4,1,1)
ax1.scatter(P[:,0], P[:,1], c=P[:,0], s=4)
ax1.set_title("A) Structural Manifold")
ax1.set_aspect('equal')

# B — STRUCTURE
ax2 = plt.subplot(4,1,2)
ax2.plot(real_s)
ax2.set_title("B) Structural Axis (Real)")

# C — RISK REAL vs SHUFFLE
ax3 = plt.subplot(4,1,3)
ax3.plot(real_r, label="Real")
ax3.plot(shuf_r, alpha=0.6, label="Shuffled")
ax3.legend()
ax3.set_title("C) Metastable Risk Comparison")

# D — DISTRIBUTION
ax4 = plt.subplot(4,1,4)
ax4.hist(real_r, bins=50, alpha=0.7, label="Real")
ax4.hist(shuf_r, bins=50, alpha=0.5, label="Shuffled")
ax4.legend()
ax4.set_title("D) Risk Distribution")

plt.tight_layout()
plt.savefig("plots/nature_figure.png", dpi=300)

# =========================
# STATISTICS
# =========================
print("\n📊 COMPARISON")

print("Real mean risk:", np.mean(real_r))
print("Shuffle mean risk:", np.mean(shuf_r))

print("Real std:", np.std(real_r))
print("Shuffle std:", np.std(shuf_r))

# simple effect size
effect = np.mean(real_r) - np.mean(shuf_r)
print("\n🔥 effect size:", effect)

if effect > 0:
    print("✅ real genome shows stronger structure than random")
else:
    print("⚠️ no clear difference")

print("\n📊 saved: plots/nature_figure.png")
print("🚀 DONE")
PYEOF

python final_analysis.py

