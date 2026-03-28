import numpy as np
import pandas as pd
import argparse
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.cluster import KMeans
from scipy.ndimage import gaussian_filter1d
from collections import Counter


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

    return score / (len(seq)/3)


# =========================
# FEATURE EXTRACTION
# =========================
def extract_features(seq, window):
    feats = []

    for i in range(0, len(seq)-window, window):
        w = seq[i:i+window]

        feats.append([
            gc(w),
            entropy(w),
            complexity(w),
            coding_score(w)
        ])

    return np.array(feats)


# =========================
# MULTISCALE
# =========================
def multiscale(seq, windows):

    signals = []

    for w in windows:
        X = extract_features(seq, w)
        X = StandardScaler().fit_transform(X)

        s = PCA(n_components=1).fit_transform(X).flatten()

        interp = np.interp(
            np.linspace(0, len(s), num=3000),
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
            parts = line.strip().split("\t")
            if len(parts) >= 5:
                genes.append((int(parts[3]), int(parts[4])))
    return genes


# =========================
# MAIN
# =========================
def main(args):

    os.makedirs("plots", exist_ok=True)

    print("🧬 loading...")
    seq = load_fasta(args.fasta)

    print("🔥 multiscale...")
    signal = multiscale(seq, [500,1500,3000,6000])

    # 🔥 smoothing pesado (ESSENCIAL)
    smooth = gaussian_filter1d(signal, sigma=40)
    smooth = (smooth - smooth.min())/(smooth.max()-smooth.min())

    # =========================
    # CLUSTER
    # =========================
    km = KMeans(n_clusters=3, random_state=42)
    domain = km.fit_predict(smooth.reshape(-1,1))

    # =========================
    # RISK
    # =========================
    risk = np.abs(np.gradient(smooth))
    risk = gaussian_filter1d(risk, sigma=8)
    risk = risk / np.max(risk)

    # =========================
    # HOTSPOTS (🔥 novo)
    # =========================
    threshold = np.percentile(risk, 95)
    hotspots = (risk > threshold).astype(int)

    # =========================
    # POSITIONS
    # =========================
    win = int(len(seq)/len(smooth))
    pos = np.arange(len(smooth)) * win

    df = pd.DataFrame({
        "pos": pos,
        "structure": smooth,
        "risk": risk,
        "domain": domain,
        "hotspot": hotspots
    })

    df.to_csv("genomic_metastablex.csv", index=False)

    # =========================
    # BED EXPORT
    # =========================
    with open("genomic_hotspots.bed","w") as f:
        for i,row in df.iterrows():
            if row.hotspot == 1:
                f.write(f"chr1\t{int(row.pos)}\t{int(row.pos+win)}\tHOTSPOT\n")

    # =========================
    # PCA (fix real)
    # =========================
    X = extract_features(seq, 3000)
    X = StandardScaler().fit_transform(X)
    P = PCA(n_components=2).fit_transform(X)

    # =========================
    # PLOTS
    # =========================
    x = df["pos"]

    # PCA correto
    plt.figure(figsize=(6,6))
    plt.scatter(P[:,0], P[:,1], c=P[:,0], s=5)
    plt.gca().set_aspect('equal')
    plt.title("Genomic Structural Manifold")
    plt.savefig("plots/pca.png", dpi=300)
    plt.close()

    # PAPER
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
    # GFF VALIDATION
    # =========================
    if args.gff:
        print("🧬 validating...")

        genes = load_gff(args.gff)

        gene_risk = []
        background_risk = []

        for _, row in df.iterrows():
            in_gene = False

            for g_start, g_end in genes:
                if g_start <= row.pos <= g_end:
                    in_gene = True
                    break

            if in_gene:
                gene_risk.append(row.risk)
            else:
                background_risk.append(row.risk)

        print("🔥 mean gene risk:", np.mean(gene_risk))
        print("🔥 mean background risk:", np.mean(background_risk))

    print("🚀 DONE")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fasta", required=True)
    parser.add_argument("--gff", default=None)

    args = parser.parse_args()
    main(args)
