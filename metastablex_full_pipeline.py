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


# =========================
# ORF HEURISTIC
# =========================
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
    positions = []

    for i in range(0, len(seq)-window, window):
        w = seq[i:i+window]

        feats.append([
            gc(w),
            entropy(w),
            complexity(w),
            coding_score(w)
        ])

        positions.append(i)

    return np.array(feats), np.array(positions)


# =========================
# MULTISCALE
# =========================
def multiscale(seq, windows):

    signals = []

    for w in windows:
        X, _ = extract_features(seq, w)
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
# GFF PARSER (opcional)
# =========================
def load_gff(path):
    genes = []
    with open(path) as f:
        for line in f:
            if line.startswith("#"):
                continue
            parts = line.strip().split("\t")
            if len(parts) >= 5:
                start = int(parts[3])
                end = int(parts[4])
                genes.append((start, end))
    return genes


# =========================
# MAIN
# =========================
def main(args):

    os.makedirs("plots", exist_ok=True)

    print("🧬 Loading FASTA...")
    seq = load_fasta(args.fasta)

    print("🔥 Multiscale signal...")
    signal = multiscale(seq, [500,1500,3000,6000])

    smooth = gaussian_filter1d(signal, sigma=20)
    smooth = (smooth - smooth.min())/(smooth.max()-smooth.min())

    print("🧠 Clustering...")
    km = KMeans(n_clusters=3, random_state=42)
    domain = km.fit_predict(smooth.reshape(-1,1))

    print("⚡ Risk...")
    risk = np.abs(np.gradient(smooth))
    risk = gaussian_filter1d(risk, sigma=5)
    risk = risk / np.max(risk)

    # =========================
    # CODING SCORE FINAL
    # =========================
    coding = []
    win = int(len(seq)/len(smooth))

    for i in range(len(smooth)):
        start = i*win
        end = start + win
        w = seq[start:end]
        coding.append(coding_score(w))

    coding = np.array(coding)

    # =========================
    # DATAFRAME
    # =========================
    df = pd.DataFrame({
        "pos": np.arange(len(smooth))*win,
        "structure": smooth,
        "risk": risk,
        "domain": domain,
        "coding_score": coding
    })

    df.to_csv("genomic_metastablex.csv", index=False)

    # =========================
    # BED EXPORT
    # =========================
    with open("genomic_metastablex.bed","w") as f:
        for i,row in df.iterrows():
            f.write(f"chr1\t{int(row.pos)}\t{int(row.pos+win)}\t{row.domain}\n")

    # =========================
    # PCA VISUAL
    # =========================
    X,_ = extract_features(seq, 3000)
    X = StandardScaler().fit_transform(X)
    P = PCA(n_components=2).fit_transform(X)

    # =========================
    # PLOTS (paper)
    # =========================
    x = df["pos"]

    plt.figure(figsize=(6,6))
    plt.scatter(P[:,0], P[:,1], s=5)
    plt.gca().set_aspect('equal')
    plt.title("Genomic Structural Manifold")
    plt.savefig("plots/pca.png", dpi=300)
    plt.close()

    fig, axs = plt.subplots(4,1, figsize=(10,10), sharex=True)

    axs[0].scatter(P[:,0], P[:,1], s=5)
    axs[0].set_title("A) Structural Manifold")

    axs[1].plot(x, smooth)
    axs[1].set_title("B) Structural Axis")

    axs[2].plot(x, risk)
    axs[2].set_title("C) Metastable Risk")

    axs[3].plot(x, coding)
    axs[3].set_title("D) Coding Potential")

    plt.tight_layout()
    plt.savefig("plots/paper.png", dpi=300)

    # =========================
    # GFF VALIDATION
    # =========================
    if args.gff:
        print("🧬 Validating with GFF...")
        genes = load_gff(args.gff)

        overlap = 0

        for g_start, g_end in genes:
            mask = (df["pos"] >= g_start) & (df["pos"] <= g_end)
            overlap += df[mask]["risk"].mean()

        print(f"🔥 Mean risk in genes: {overlap/len(genes):.4f}")

    print("🚀 DONE")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fasta", required=True)
    parser.add_argument("--gff", default=None)

    args = parser.parse_args()
    main(args)
