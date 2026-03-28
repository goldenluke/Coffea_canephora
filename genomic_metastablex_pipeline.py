import argparse
import numpy as np
import pandas as pd
import os

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

from collections import Counter
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.ndimage import gaussian_filter1d

from metastablex.qwan.runner import run_qwan


# =========================
# FASTA
# =========================
def load_fasta(path):
    seq = ""
    with open(path, "r") as f:
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
    probs = [v / len(seq) for v in counts.values()]
    return -sum(p * np.log2(p + 1e-9) for p in probs)


def complexity(seq):
    return len(set(seq)) / len(seq)


def kmer_freq(seq, k=3):
    kmers = [seq[i:i+k] for i in range(len(seq)-k+1)]
    counts = Counter(kmers)
    total = sum(counts.values())
    return {k: v / total for k, v in counts.items()}


# =========================
# DATASET
# =========================
def build_dataset(sequence, window):
    data = []

    for i in range(0, len(sequence) - window, window):
        w = sequence[i:i+window]

        features = {
            "start": i,
            "end": i + window,
            "gc": gc_content(w),
            "entropy": entropy(w),
            "complexity": complexity(w),
        }

        features.update(kmer_freq(w))
        data.append(features)

    return pd.DataFrame(data).fillna(0)


# =========================
# METASTABLEX
# =========================
def run_metastablex_series(pca1, step=15):
    risks = np.zeros(len(pca1))

    print(f"⚡ MetastableX step={step}")

    for i in range(0, len(pca1), step):
        if i % 200 == 0:
            print(f"{i}/{len(pca1)}")

        window = pca1[max(0, i-5):i+5]

        if len(window) < 5:
            continue

        try:
            res = run_qwan(window)
            risks[i] = res.get("risk", 0)
        except:
            continue

    # interpolação
    risks = pd.Series(risks).replace(0, np.nan).interpolate().fillna(0).values

    # normalização
    if np.max(risks) > 0:
        risks = risks / np.max(risks)

    return risks


# =========================
# PLOTS (CORRIGIDOS)
# =========================
def make_plots(df):
    os.makedirs("plots", exist_ok=True)

    x = np.arange(len(df))

    plt.rcParams.update({
        "font.size": 10,
        "figure.figsize": (10, 4)
    })

    # PCA
    plt.figure()
    plt.scatter(df["pca1"], df["pca2"], c=df["cluster"], s=6)
    plt.title("Genomic Structural Manifold (PCA)")
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.axis("equal")
    plt.tight_layout()
    plt.savefig("plots/pca.png", dpi=300)
    plt.close()

    # Structure (corrigido)
    plt.figure()
    plt.plot(x, df["cluster_smooth"], linewidth=1.2, label="cluster")
    plt.plot(x, df["instability"], linestyle="--", linewidth=1, label="instability")
    plt.legend()
    plt.title("Structural Domains")
    plt.xlabel("Genomic position")
    plt.tight_layout()
    plt.savefig("plots/structure.png", dpi=300)
    plt.close()

    # Risk
    plt.figure()
    plt.plot(x, df["meta_risk"], linewidth=1.5)
    plt.title("Metastable Risk (normalized)")
    plt.xlabel("Genomic position")
    plt.tight_layout()
    plt.savefig("plots/risk.png", dpi=300)
    plt.close()

    # FIGURA FINAL
    fig, axs = plt.subplots(3, 1, figsize=(10, 8), sharex=True)

    axs[0].scatter(df["pca1"], df["pca2"], c=df["cluster"], s=5)
    axs[0].set_title("A) PCA")
    axs[0].axis("equal")

    axs[1].plot(x, df["cluster_smooth"])
    axs[1].set_title("B) Structural Domains")

    axs[2].plot(x, df["meta_risk"])
    axs[2].set_title("C) Metastable Risk")

    axs[2].set_xlabel("Genomic Position")

    plt.tight_layout()
    plt.savefig("plots/paper.png", dpi=300)
    plt.close()

    print("📊 plots salvos em /plots")


# =========================
# MAIN
# =========================
def main(args):
    print("🧬 Loading FASTA...")
    seq = load_fasta(args.fasta)

    print("🔬 Building dataset...")
    df = build_dataset(seq, args.window)

    features = [c for c in df.columns if c not in ["start", "end"]]
    X = df[features].values

    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    print("🤖 Clustering...")
    kmeans = KMeans(n_clusters=args.k, random_state=42)
    df["cluster"] = kmeans.fit_predict(X_scaled)

    # 🔥 suavização CORRETA
    smooth = gaussian_filter1d(df["cluster"].astype(float), sigma=2)
    df["cluster_smooth"] = np.round(smooth)

    print("📉 PCA...")
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    df["pca1"] = X_pca[:, 0]
    df["pca2"] = X_pca[:, 1]

    print("⚡ Instability...")
    df["instability"] = np.concatenate([[0], np.abs(np.diff(df["cluster_smooth"]))])

    print("🔥 MetastableX...")
    df["meta_risk"] = run_metastablex_series(df["pca1"].values)

    print("💾 Saving CSV...")
    df.to_csv("genomic_metastablex.csv", index=False)

    print("📊 Plotting...")
    make_plots(df)

    print("🎉 DONE")


# =========================
# CLI
# =========================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fasta", required=True)
    parser.add_argument("--window", type=int, default=3000)
    parser.add_argument("--k", type=int, default=3)

    args = parser.parse_args()
    main(args)

