#!/usr/bin/env bash
set -e

echo "🧬 MetastableX + E. coli (FULL PIPELINE)"

mkdir -p data plots

# =========================
# DOWNLOAD (E. coli)
# =========================
echo "⬇️ downloading genome..."
wget -q -O data/ecoli.fna.gz https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_genomic.fna.gz

echo "⬇️ downloading GFF..."
wget -q -O data/ecoli.gff.gz https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/000/005/845/GCF_000005845.2_ASM584v2/GCF_000005845.2_ASM584v2_genomic.gff.gz

gunzip -f data/ecoli.fna.gz
gunzip -f data/ecoli.gff.gz

# =========================
# PIPELINE + ENRICHMENT
# =========================
cat << 'PYEOF' > ecoli_pipeline.py
import numpy as np
import pandas as pd
from collections import Counter
import os

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.ndimage import gaussian_filter1d
from math import comb

print("🧬 loading sequence...")

# =========================
# FASTA
# =========================
def load_fasta(path):
    seq = ""
    with open(path) as f:
        for line in f:
            if not line.startswith(">"):
                seq += line.strip().upper()
    return seq

seq = load_fasta("data/ecoli.fna")

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
X = extract(seq, 1000)
X = StandardScaler().fit_transform(X)

signal = PCA(n_components=1).fit_transform(X).flatten()
smooth = gaussian_filter1d(signal, sigma=10)
smooth = (smooth - smooth.min())/(smooth.max()-smooth.min())

risk = np.abs(np.gradient(smooth))
risk = gaussian_filter1d(risk, sigma=3)
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
# LOAD GFF
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

genes = load_gff("data/ecoli.gff")

print("🧬 genes:", len(genes))

# =========================
# GENE COVERAGE
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
else:
    print("❌ no enrichment")

print("\n🚀 DONE")
PYEOF

python ecoli_pipeline.py

