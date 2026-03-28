import argparse
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import os
from collections import Counter
from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from scipy.ndimage import gaussian_filter1d

# MetastableX
from metastablex.metastablex.qwan.runner import run_qwan


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
def build_dataset(sequence, window, kmer_size=3):
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

        kmers = kmer_freq(w, kmer_size)
        features.update(kmers)

        data.append(features)

    return pd.DataFrame(data).fillna(0)


# =========================
# METASTABLEX
# =========================
def run_metastablex_series(X):
    risks = []
    regimes = []

    for i in range(len(X)):
        window = X[max(0, i-5):i+5]

        if len(window) < 5:
            risks.append(0)
            regimes.append("unknown")
            continue

        series = window[:, 0]

        try:
            res = run_qwan(series)
            risks.append(res.get("risk", 0))
            regimes.append(res.get("regime", "unknown"))
        except:
            risks.append(0)
            regimes.append("fail")

    return risks, regimes


# =========================
# PLOTS (PAPER LEVEL)
# =========================
def make_plots(df):
    os.makedirs("plots", exist_ok=True)

    plt.rcParams.update({
        "font.size": 10,
        "figure.figsize": (10, 4),
        "axes.spines.top": False,
        "axes.spines.right": False
    })

    x = np.arange(len(df))

    # =========================
    # PCA
    # =========================
    plt.figure()
    plt.scatter(df["pca1"], df["pca2"], c=df["cluster"], s=10)
    plt.xlabel("PC1")
    plt.ylabel("PC2")
    plt.title("Genomic Structural Manifold (PCA)")
    plt.tight_layout()
    plt.savefig("plots/pca_clusters.png", dpi=300)
    plt.close()

    # =========================
    # CLUSTERS + INSTABILITY
    # =========================
    plt.figure()
    plt.plot(x, df["cluster_smooth"], linewidth=1, label="Cluster (smoothed)")
    plt.plot(x, df["instability"], linewidth=1, linestyle="--", label="Instability")
    plt.xlabel("Genomic position (windows)")
    plt.ylabel("State")
    plt.title("Structural Regimes and Instability")
    plt.legend()
    plt.tight_layout()
    plt.savefig("plots/structure_instability.png", dpi=300)
    plt.close()

    # =========================
    # METASTABLE RISK
    # =========================
    plt.figure()
    plt.plot(x, df["meta_risk"], linewidth=1.5)
    plt.xlabel("Genomic position (windows)")
    plt.ylabel("Risk")
    plt.title("Metastable Risk Profile")
    plt.tight_layout()
    plt.savefig("plots/metastable_risk.png", dpi=300)
    plt.close()

    # =========================
    # FINAL COMBINED (FIGURA DE PAPER)
    # =========================
    fig, axs = plt.subplots(3, 1, sharex=True, figsize=(10, 8))

    axs[0].scatter(df["pca1"], df["pca2"], c=df["cluster"], s=5)
    axs[0].set_title("A) PCA Structural Space")

    axs[1].plot(x, df["cluster_smooth"], label="Cluster")
    axs[1].plot(x, df["instability"], linestyle="--", label="Instability")
    axs[1].set_title("B) Structural Regimes")
    axs[1].legend()

    axs[2].plot(x, df["meta_risk"])
    axs[2].set_title("C) Metastable Risk")

    axs[2].set_xlabel("Genomic Position")

    plt.tight_layout()
    plt.savefig("plots/figure_paper.png", dpi=300)
    plt.close()


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

    df["cluster_smooth"] = gaussian_filter1d(df["cluster"], sigma=2)

    print("📉 PCA...")
    pca = PCA(n_components=2)
    X_pca = pca.fit_transform(X_scaled)

    df["pca1"] = X_pca[:, 0]
    df["pca2"] = X_pca[:, 1]

    print("⚡ Instability...")
    transitions = np.abs(np.diff(df["cluster_smooth"]))
    df["instability"] = np.concatenate([[0], transitions])

    print("🔥 MetastableX...")
    risks, regimes = run_metastablex_series(X_pca)

    df["meta_risk"] = risks
    df["meta_regime"] = regimes

    print("💾 Saving...")
    df.to_csv("genomic_metastablex.csv", index=False)

    with open("genomic_metastablex.bed", "w") as f:
        for _, row in df.iterrows():
            f.write(f"chr1\t{int(row.start)}\t{int(row.end)}\tcluster_{int(row.cluster)}\n")

    print("📊 Plotting...")
    make_plots(df)

    print("✅ DONE")


# =========================
# CLI
# =========================
if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fasta", required=True)
    parser.add_argument("--window", type=int, default=2000)
    parser.add_argument("--k", type=int, default=3)

    args = parser.parse_args()
    main(args)

