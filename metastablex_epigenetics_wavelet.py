import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from collections import Counter
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.ndimage import gaussian_filter1d
from scipy.stats import binomtest
import pywt
import os, requests, gzip

os.makedirs("data", exist_ok=True)
os.makedirs("plots", exist_ok=True)

# =========================
# DOWNLOAD DATA (Arabidopsis)
# =========================
def download(url, path):
    if not os.path.exists(path):
        print("⬇ downloading:", path)
        r = requests.get(url)
        with open(path, "wb") as f:
            f.write(r.content)

# genome
download(
"https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/735/GCF_000001735.4_TAIR10.1/GCF_000001735.4_TAIR10.1_genomic.fna.gz",
"data/genome.fa.gz"
)

# decompress
if not os.path.exists("data/genome.fa"):
    with gzip.open("data/genome.fa.gz", "rb") as f_in:
        with open("data/genome.fa", "wb") as f_out:
            f_out.write(f_in.read())

# =========================
# LOAD FASTA
# =========================
def load_fasta(path, max_len=5_000_000):
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

    return X, smooth, risk

# =========================
# WAVELET ANALYSIS
# =========================
def wavelet_analysis(signal):

    coeffs = pywt.wavedec(signal, 'db4', level=5)

    energies = []
    for c in coeffs:
        energies.append(np.sum(c**2))

    return coeffs, energies

# =========================
# PEAK DETECTION
# =========================
def detect_peaks(risk, threshold=0.8):
    return np.where(risk > threshold)[0]

# =========================
# FAKE EPIGENETIC SIGNAL (proxy)
# =========================
def generate_fake_epigenetics(n):
    # simulate open chromatin regions
    signal = np.random.rand(n)
    signal = gaussian_filter1d(signal, sigma=10)
    return signal

# =========================
# MAIN
# =========================
print("🧬 loading genome...")
seq = load_fasta("data/genome.fa")

print("⚙ running pipeline...")
X, struct, risk = run_pipeline(seq)

# =========================
# SHUFFLE CONTROL
# =========================
print("🎲 shuffle...")
seq_list = list(seq)
np.random.shuffle(seq_list)
seq_shuf = "".join(seq_list)

_, struct_s, risk_s = run_pipeline(seq_shuf)

# =========================
# WAVELET
# =========================
print("🌊 wavelet...")
coeffs, energies = wavelet_analysis(struct)

# =========================
# PEAKS
# =========================
peaks = detect_peaks(risk)
print("🔥 peaks:", len(peaks))

# =========================
# EPIGENETIC PROXY
# =========================
epi = generate_fake_epigenetics(len(risk))

epi_regions = np.where(epi > 0.7)[0]

# overlap
overlap = len(set(peaks) & set(epi_regions))
n = len(peaks)
p = len(epi_regions)/len(risk)

print("📊 overlap:", overlap)

# =========================
# STAT TEST
# =========================
if p > 0 and p < 1:
    res = binomtest(overlap, n, p, alternative='greater')
    print("📉 p-value:", res.pvalue)

# =========================
# PLOTS
# =========================

# STRUCTURE
plt.figure()
plt.plot(struct)
plt.title("Structural Axis")
plt.savefig("plots/structure.png", dpi=300)
plt.close()

# RISK
plt.figure()
plt.plot(risk, label="Real")
plt.plot(risk_s, label="Shuffle", alpha=0.6)
plt.legend()
plt.title("Metastable Risk")
plt.savefig("plots/risk.png", dpi=300)
plt.close()

# DISTRIBUTION
plt.figure()
sns.kdeplot(risk, label="Real")
sns.kdeplot(risk_s, label="Shuffle")
plt.legend()
plt.savefig("plots/distribution.png", dpi=300)
plt.close()

# WAVELET ENERGY
plt.figure()
plt.plot(energies)
plt.title("Wavelet Energy by Scale")
plt.savefig("plots/wavelet.png", dpi=300)
plt.close()

# PEAKS
plt.figure()
plt.plot(risk)
plt.scatter(peaks, risk[peaks])
plt.title("Hotspots")
plt.savefig("plots/hotspots.png", dpi=300)
plt.close()

print("🚀 DONE")

