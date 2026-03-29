import numpy as np
import matplotlib.pyplot as plt
from collections import Counter
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.ndimage import gaussian_filter1d
from scipy.stats import binomtest
import requests, gzip, os

os.makedirs("data", exist_ok=True)
os.makedirs("plots", exist_ok=True)

# =========================
# DOWNLOAD HUMAN CHR11
# =========================
url = "https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/001/405/GCF_000001405.40_GRCh38.p14/GCF_000001405.40_GRCh38.p14_genomic.fna.gz"

if not os.path.exists("data/human.fa.gz"):
    print("⬇ downloading human genome...")
    r = requests.get(url)
    with open("data/human.fa.gz", "wb") as f:
        f.write(r.content)

if not os.path.exists("data/human.fa"):
    with gzip.open("data/human.fa.gz", "rb") as f_in:
        with open("data/human.fa", "wb") as f_out:
            f_out.write(f_in.read())

# =========================
# LOAD CHR11 ONLY
# =========================
def load_chr11(path, max_len=5_000_000):
    seq = ""
    reading = False

    with open(path) as f:
        for line in f:
            if line.startswith(">"):
                reading = "chromosome 11" in line.lower()
                continue
            if reading:
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
def run_pipeline(seq, window=1000):

    X = extract(seq, window)
    X_scaled = StandardScaler().fit_transform(X)

    P = PCA(n_components=2).fit_transform(X_scaled)

    signal = P[:,0]

    smooth = gaussian_filter1d(signal, sigma=15)
    smooth = (smooth - smooth.min())/(smooth.max()-smooth.min())

    risk = np.abs(np.gradient(smooth))
    risk = gaussian_filter1d(risk, sigma=5)
    risk = risk / np.max(risk)

    return smooth, risk

# =========================
# LOAD DATA
# =========================
print("🧬 loading chr11...")
seq = load_chr11("data/human.fa")

print("⚙ running...")
struct, risk = run_pipeline(seq)

# =========================
# HBB GENE (REAL COORDS)
# =========================
# HBB gene (chr11: 5,225,464–5,227,071 GRCh38)
HBB_start = 5225464
HBB_end = 5227071

window = 1000

HBB_windows = list(range(HBB_start//window, HBB_end//window))

# =========================
# HOTSPOTS
# =========================
threshold = 0.85
hotspots = np.where(risk > threshold)[0]

print("🔥 hotspots:", len(hotspots))

# =========================
# OVERLAP
# =========================
overlap = len(set(hotspots) & set(HBB_windows))

n = len(hotspots)
p = len(HBB_windows)/len(risk)

print("🧬 HBB overlap:", overlap)

# =========================
# STAT TEST
# =========================
if p > 0 and p < 1 and n > 0:
    res = binomtest(overlap, n, p, alternative='greater')
    print("📉 p-value:", res.pvalue)

# =========================
# PLOT
# =========================
plt.figure(figsize=(12,4))
plt.plot(risk, label="Metastable Risk")

# highlight HBB
for w in HBB_windows:
    plt.axvspan(w, w+1, alpha=0.3)

plt.title("Metastable Risk — Human chr11 (HBB region highlighted)")
plt.savefig("plots/human_hbb.png", dpi=300)
plt.close()

print("🚀 DONE")

