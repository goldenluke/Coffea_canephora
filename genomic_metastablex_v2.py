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


def load_fasta(path):
    seq = ""
    with open(path) as f:
        for line in f:
            if not line.startswith(">"):
                seq += line.strip().upper()
    return seq


def entropy(seq):
    counts = Counter(seq)
    probs = [v/len(seq) for v in counts.values()]
    return -sum(p*np.log2(p+1e-9) for p in probs)


def gc(seq):
    return (seq.count("G")+seq.count("C"))/len(seq)


def build(seq, window):
    data = []
    for i in range(0, len(seq)-window, window):
        w = seq[i:i+window]
        data.append({
            "pos": i,
            "gc": gc(w),
            "entropy": entropy(w),
            "complexity": len(set(w))/len(w)
        })
    return pd.DataFrame(data)


def main(args):
    os.makedirs("plots", exist_ok=True)

    seq = load_fasta(args.fasta)
    df = build(seq, args.window)

    X = df.drop(columns=["pos"]).values
    X = StandardScaler().fit_transform(X)

    pca = PCA(n_components=2)
    P = pca.fit_transform(X)

    df["pca1"] = P[:,0]
    df["pca2"] = P[:,1]

    # 🔥 smoothing forte (multi-scale simplificado)
    smooth = gaussian_filter1d(df["pca1"], sigma=10)
    smooth = gaussian_filter1d(smooth, sigma=5)

    smooth = (smooth - smooth.min())/(smooth.max()-smooth.min())

    # 🔥 cluster contínuo
    km = KMeans(n_clusters=3, random_state=42)
    df["domain"] = km.fit_predict(smooth.reshape(-1,1))

    # 🔥 risco REAL
    risk = np.abs(np.gradient(smooth))
    risk = gaussian_filter1d(risk, sigma=3)
    risk = risk / np.max(risk)

    df["risk"] = risk

    df.to_csv("genomic_metastablex.csv", index=False)

    x = np.arange(len(df))

    # PCA
    plt.figure(figsize=(6,6))
    plt.scatter(df["pca1"], df["pca2"], c=df["domain"], s=5)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig("plots/pca.png", dpi=300)
    plt.close()

    # STRUCTURE
    plt.figure()
    plt.plot(x, smooth)
    plt.savefig("plots/structure.png", dpi=300)
    plt.close()

    # RISK
    plt.figure()
    plt.plot(x, risk)
    plt.savefig("plots/risk.png", dpi=300)
    plt.close()

    # PAPER
    fig, axs = plt.subplots(3,1, figsize=(8,8), sharex=True)

    axs[0].scatter(df["pca1"], df["pca2"], c=df["domain"], s=5)
    axs[0].set_aspect('equal', adjustable='box')

    axs[1].plot(x, smooth)
    axs[2].plot(x, risk)

    plt.tight_layout()
    plt.savefig("plots/paper.png", dpi=300)

    print("🔥 versão científica pronta")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fasta", required=True)
    parser.add_argument("--window", type=int, default=3000)
    args = parser.parse_args()

    main(args)
