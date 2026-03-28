import argparse
import numpy as np
import pandas as pd
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from collections import Counter
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.ndimage import gaussian_filter1d


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
def gc_content(seq):
    return (seq.count("G") + seq.count("C")) / len(seq)


def entropy(seq):
    counts = Counter(seq)
    probs = [v/len(seq) for v in counts.values()]
    return -sum(p*np.log2(p+1e-9) for p in probs)


def complexity(seq):
    return len(set(seq)) / len(seq)


def kmer_freq(seq, k=3):
    kmers = [seq[i:i+k] for i in range(len(seq)-k+1)]
    counts = Counter(kmers)
    total = sum(counts.values())
    return {k: v/total for k, v in counts.items()}


# =========================
# DATASET
# =========================
def build_dataset(seq, window):
    data = []

    for i in range(0, len(seq)-window, window):
        w = seq[i:i+window]

        f = {
            "pos": i,
            "gc": gc_content(w),
            "entropy": entropy(w),
            "complexity": complexity(w),
        }

        f.update(kmer_freq(w))
        data.append(f)

    return pd.DataFrame(data).fillna(0)


# =========================
# MAIN
# =========================
def main(args):

    os.makedirs("plots", exist_ok=True)

    print("🧬 Loading...")
    seq = load_fasta(args.fasta)

    print("🔬 Features...")
    df = build_dataset(seq, args.window)

    X = df.drop(columns=["pos"]).values

    scaler = StandardScaler()
    X = scaler.fit_transform(X)

    print("📉 PCA...")
    pca = PCA(n_components=2)
    P = pca.fit_transform(X)

    df["pca1"] = P[:,0]
    df["pca2"] = P[:,1]

    # =========================
    # 🔥 ESTRUTURA CONTÍNUA
    # =========================
    smooth = gaussian_filter1d(df["pca1"], sigma=3)

    # normaliza
    smooth = (smooth - smooth.min()) / (smooth.max() - smooth.min())

    # discretiza suavemente (domínios)
    domains = np.digitize(smooth, bins=[0.33, 0.66])
    df["domain"] = domains

    # =========================
    # ⚡ INSTABILIDADE REAL
    # =========================
    grad = np.abs(np.gradient(smooth))
    grad = grad / np.max(grad)

    df["risk"] = grad

    # =========================
    # 💾 SAVE
    # =========================
    df.to_csv("genomic_metastablex.csv", index=False)

    # =========================
    # 📊 PLOTS (FIXOS)
    # =========================
    x = np.arange(len(df))

    plt.rcParams.update({
        "figure.figsize": (10,4),
        "font.size": 10
    })

    # PCA
    plt.figure()
    plt.scatter(df["pca1"], df["pca2"], c=df["domain"], s=6)
    plt.axis("equal")
    plt.title("Genomic Structural Manifold")
    plt.savefig("plots/pca.png", dpi=300)
    plt.close()

    # STRUCTURE
    plt.figure()
    plt.plot(x, smooth, linewidth=1.5)
    plt.title("Continuous Structural Axis")
    plt.savefig("plots/structure.png", dpi=300)
    plt.close()

    # RISK
    plt.figure()
    plt.plot(x, df["risk"], linewidth=1.5)
    plt.title("Metastable Risk")
    plt.savefig("plots/risk.png", dpi=300)
    plt.close()

    # PAPER FIGURE
    fig, axs = plt.subplots(3,1, figsize=(10,8), sharex=True)

    axs[0].scatter(df["pca1"], df["pca2"], c=df["domain"], s=5)
    axs[0].axis("equal")
    axs[0].set_title("A) Structural Manifold")

    axs[1].plot(x, smooth)
    axs[1].set_title("B) Structural Axis")

    axs[2].plot(x, df["risk"])
    axs[2].set_title("C) Metastable Risk")

    axs[2].set_xlabel("Genomic Position")

    plt.tight_layout()
    plt.savefig("plots/paper.png", dpi=300)
    plt.close()

    print("🔥 DONE (AGORA SIM)")

# =========================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fasta", required=True)
    parser.add_argument("--window", type=int, default=3000)

    args = parser.parse_args()
    main(args)

