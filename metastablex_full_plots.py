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
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    pca = PCA(n_components=2)
    P = pca.fit_transform(X_scaled)

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
# 1. PCA
# =========================
plt.figure()
plt.scatter(P[:,0], P[:,1], c=P[:,0], s=4)
plt.title("PCA Manifold")
plt.savefig("plots/pca.png", dpi=300)
plt.close()

# =========================
# 2. STRUCTURE
# =========================
plt.figure()
plt.plot(real_s)
plt.title("Structural Axis")
plt.savefig("plots/structure.png", dpi=300)
plt.close()

# =========================
# 3. RISK
# =========================
plt.figure()
plt.plot(real_r, label="Real")
plt.plot(shuf_r, label="Shuffle", alpha=0.6)
plt.legend()
plt.title("Metastable Risk")
plt.savefig("plots/risk.png", dpi=300)
plt.close()

# =========================
# 4. DISTRIBUTION
# =========================
plt.figure()
sns.kdeplot(real_r, label="Real", fill=True)
sns.kdeplot(shuf_r, label="Shuffle", fill=True)
plt.legend()
plt.title("Risk Distribution")
plt.savefig("plots/distribution.png", dpi=300)
plt.close()

# =========================
# 5. DELTA
# =========================
delta = real_r - shuf_r

plt.figure()
plt.plot(delta)
plt.axhline(0)
plt.title("Delta Risk (Real - Shuffle)")
plt.savefig("plots/delta.png", dpi=300)
plt.close()

# =========================
# 6. AUTOCORRELATION 🔥
# =========================
def autocorr(x):
    return np.correlate(x, x, mode='full')[len(x)-1:]

plt.figure()
plt.plot(autocorr(real_r)[:1000], label="Real")
plt.plot(autocorr(shuf_r)[:1000], label="Shuffle")
plt.legend()
plt.title("Autocorrelation")
plt.savefig("plots/autocorrelation.png", dpi=300)
plt.close()

# =========================
# 7. HEATMAP FEATURES
# =========================
plt.figure()
sns.heatmap(X[:500], cmap="viridis")
plt.title("Feature Heatmap")
plt.savefig("plots/heatmap.png", dpi=300)
plt.close()

# =========================
# 8. CORRELATION MATRIX
# =========================
plt.figure()
sns.heatmap(np.corrcoef(X.T), annot=True)
plt.title("Feature Correlation")
plt.savefig("plots/correlation.png", dpi=300)
plt.close()

# =========================
# 9. FFT (PERIODICIDADE)
# =========================
fft = np.abs(np.fft.fft(real_r))

plt.figure()
plt.plot(fft[:1000])
plt.title("Frequency Spectrum")
plt.savefig("plots/fft.png", dpi=300)
plt.close()

# =========================
# 10. CUMULATIVE PROFILE
# =========================
plt.figure()
plt.plot(np.cumsum(real_r))
plt.title("Cumulative Risk")
plt.savefig("plots/cumulative.png", dpi=300)
plt.close()

print("🔥 ALL PLOTS GENERATED → /plots")

