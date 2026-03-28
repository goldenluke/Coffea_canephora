#!/usr/bin/env bash
set -e

echo "🚀 MetastableX Auto Pipeline"

# =========================
# CONFIG
# =========================
GENOME_URL="https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/003/713/225/GCF_003713225.1_Canephora_v1.0/GCF_003713225.1_Canephora_v1.0_genomic.fna.gz"
GFF_URL="https://ftp.ncbi.nlm.nih.gov/genomes/all/GCF/003/713/225/GCF_003713225.1_Canephora_v1.0/GCF_003713225.1_Canephora_v1.0_genomic.gff.gz"

mkdir -p data plots

# =========================
# DOWNLOAD
# =========================
echo "⬇️ downloading genome..."
wget -q -O data/genome.fna.gz $GENOME_URL

echo "⬇️ downloading GFF..."
wget -q -O data/genes.gff.gz $GFF_URL

# =========================
# EXTRACT
# =========================
echo "📦 extracting..."
gunzip -f data/genome.fna.gz
gunzip -f data/genes.gff.gz

# =========================
# PYTHON PIPELINE
# =========================
cat << 'PYEOF' > metastablex_pipeline.py
import numpy as np
import pandas as pd
import os
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy.ndimage import gaussian_filter1d


# =========================
# FASTA (single chromosome)
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

def coding_score(seq):
    start = ["ATG"]
    stop = ["TAA","TAG","TGA"]
    score = 0

    for i in range(0, len(seq)-3, 3):
        codon = seq[i:i+3]
        if codon in start:
            score += 2
        if codon in stop:
            score -= 1

    return score / (len(seq)/3 + 1e-9)


# =========================
# FEATURES EXTRACTION
# =========================
def extract(seq, window):
    feats = []
    for i in range(0, len(seq)-window, window):
        w = seq[i:i+window]
        feats.append([gc(w), entropy(w), complexity(w), coding_score(w)])
    return np.array(feats)


# =========================
# MULTISCALE
# =========================
def multiscale(seq):
    signals = []

    for w in [500,1500,3000,6000]:
        X = extract(seq, w)
        X = StandardScaler().fit_transform(X)
        s = PCA(n_components=1).fit_transform(X).flatten()

        interp = np.interp(
            np.linspace(0, len(s), 3000),
            np.arange(len(s)),
            s
        )

        signals.append(interp)

    return np.mean(signals, axis=0)


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
            if len(p) > 4:
                genes.append((int(p[3]), int(p[4])))
    return genes


# =========================
# RUN
# =========================
print("🧬 loading sequence...")
seq = load_fasta("data/genome.fna")

print("🔥 computing multiscale...")
signal = multiscale(seq)

smooth = gaussian_filter1d(signal, sigma=40)
smooth = (smooth - smooth.min())/(smooth.max()-smooth.min())

risk = np.abs(np.gradient(smooth))
risk = gaussian_filter1d(risk, sigma=8)
risk = risk / np.max(risk)

threshold = np.percentile(risk, 95)
hotspots = (risk > threshold).astype(int)

win = int(len(seq)/len(smooth))
pos = np.arange(len(smooth)) * win

df = pd.DataFrame({
    "pos": pos,
    "structure": smooth,
    "risk": risk,
    "hotspot": hotspots
})

df.to_csv("genomic_metastablex.csv", index=False)

# =========================
# BED
# =========================
with open("genomic_hotspots.bed","w") as f:
    for i,row in df.iterrows():
        if row.hotspot == 1:
            f.write(f"chr1\t{int(row.pos)}\t{int(row.pos+win)}\tHOTSPOT\n")

# =========================
# PCA
# =========================
X = extract(seq, 3000)
X = StandardScaler().fit_transform(X)
P = PCA(n_components=2).fit_transform(X)

plt.figure(figsize=(6,6))
plt.scatter(P[:,0], P[:,1], c=P[:,0], s=5)
plt.gca().set_aspect('equal')
plt.title("Genomic Structural Manifold")
plt.savefig("plots/pca.png", dpi=300)
plt.close()

# =========================
# PAPER FIG
# =========================
x = df["pos"]

fig, axs = plt.subplots(3,1, figsize=(10,8), sharex=True)

axs[0].scatter(P[:,0], P[:,1], c=P[:,0], s=5)
axs[0].set_title("A) Structural Manifold")
axs[0].set_aspect('equal')

axs[1].plot(x, smooth)
axs[1].set_title("B) Structural Axis")

axs[2].plot(x, risk)
axs[2].scatter(x[hotspots==1], risk[hotspots==1], s=5)
axs[2].set_title("C) Metastable Risk + Hotspots")

plt.tight_layout()
plt.savefig("plots/paper.png", dpi=300)

# =========================
# VALIDATION
# =========================
if os.path.exists("data/genes.gff"):
    print("🧬 validating...")

    genes = load_gff("data/genes.gff")

    gene_risk = []
    bg_risk = []

    for _, row in df.iterrows():
        in_gene = any(s <= row.pos <= e for s,e in genes)

        if in_gene:
            gene_risk.append(row.risk)
        else:
            bg_risk.append(row.risk)

    print("🔥 gene risk:", np.mean(gene_risk))
    print("🔥 background:", np.mean(bg_risk))

print("✅ DONE")
PYEOF

# =========================
# RUN
# =========================
echo "⚙️ running pipeline..."
python metastablex_pipeline.py

echo "📊 outputs:"
echo "- plots/pca.png"
echo "- plots/paper.png"
echo "- genomic_metastablex.csv"
echo "- genomic_hotspots.bed"

