import numpy as np
import pandas as pd
from collections import Counter
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.ndimage import gaussian_filter1d
from math import comb

print("🌱 loading sequence...")

# =========================
# FASTA (limitado)
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

seq = load_fasta("data/arabidopsis.fa")

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
# STRUCTURE
# =========================
X = extract(seq, 1500)
X = StandardScaler().fit_transform(X)

signal = PCA(n_components=1).fit_transform(X).flatten()

smooth = gaussian_filter1d(signal, sigma=20)
smooth = (smooth - smooth.min())/(smooth.max()-smooth.min())

risk = np.abs(np.gradient(smooth))
risk = gaussian_filter1d(risk, sigma=6)
risk = risk / np.max(risk)

threshold = np.percentile(risk, 95)
hotspots = (risk > threshold).astype(int)

win = int(len(seq)/len(smooth))
pos = np.arange(len(smooth)) * win

df = pd.DataFrame({
    "pos": pos,
    "risk": risk,
    "hotspot": hotspots
})

# =========================
# GFF (genes only)
# =========================
def load_gff(path):
    genes = []
    with open(path) as f:
        for line in f:
            if line.startswith("#"):
                continue
            p = line.split("\t")
            if len(p) > 4 and p[2] == "gene":
                genes.append((int(p[3]), int(p[4])))
    return genes

genes = load_gff("data/arabidopsis.gff")

print("🌱 genes:", len(genes))

# =========================
# COVERAGE
# =========================
genome_size = df["pos"].max()
gene_bases = sum(e - s for s,e in genes)
gene_fraction = gene_bases / genome_size

# =========================
# OVERLAP
# =========================
def in_gene(pos):
    return any(s <= pos <= e for s,e in genes)

df["in_gene"] = df["pos"].apply(in_gene)

hot = df[df.hotspot == 1]

k = hot["in_gene"].sum()
n = len(hot)
p = gene_fraction

print("\n🔥 hotspots:", n)
print("🔥 in genes:", k)
print("📊 expected:", round(p,3))
print("📊 observed:", round(k/n,3))

# =========================
# BINOMIAL
# =========================
def binom(k,n,p):
    prob = 0
    for i in range(k,n+1):
        prob += comb(n,i)*(p**i)*((1-p)**(n-i))
    return prob

pval = binom(k,n,p)

print("\n📉 p-value:", pval)

if pval < 0.05:
    print("✅ enrichment detected")
elif pval < 0.1:
    print("⚠️ weak enrichment")
else:
    print("❌ no enrichment")

print("\n🚀 DONE")
