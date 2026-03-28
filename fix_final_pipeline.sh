#!/usr/bin/env bash
set -e

cat << 'PYEOF' > fix_pipeline.py
import numpy as np
import pandas as pd
from collections import Counter
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.ndimage import gaussian_filter1d
from scipy.stats import binomtest

print("🌱 loading sequence...")

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

seq = load_fasta("data/arabidopsis.fa")
SEQ_LEN = len(seq)

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
# GFF
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

# 🔥 FILTRO CRÍTICO
genes = [(s,e) for s,e in genes if s < SEQ_LEN]

print("🌱 filtered genes:", len(genes))

# =========================
# MERGE
# =========================
genes_sorted = sorted(genes)
merged = []

for s,e in genes_sorted:
    if not merged or s > merged[-1][1]:
        merged.append([s,e])
    else:
        merged[-1][1] = max(merged[-1][1], e)

gene_bases = sum(e - s for s,e in merged)
gene_fraction = gene_bases / SEQ_LEN

print("📏 gene fraction:", round(gene_fraction,4))

# =========================
# OVERLAP
# =========================
def in_gene(pos):
    return any(s <= pos <= e for s,e in merged)

df["in_gene"] = df["pos"].apply(in_gene)

hot = df[df.hotspot == 1]

k = int(hot["in_gene"].sum())
n = len(hot)
p = gene_fraction

print("\n🔥 hotspots:", n)
print("🔥 in genes:", k)
print("📊 expected:", round(p,4))
print("📊 observed:", round(k/n,4))

# =========================
# BINOMIAL TEST
# =========================
res = binomtest(k, n, p, alternative='greater')
print("\n📉 p-value:", res.pvalue)

if res.pvalue < 0.05:
    print("✅ enrichment detected")
else:
    print("❌ no enrichment")

print("\n🚀 DONE")
PYEOF

python fix_pipeline.py

