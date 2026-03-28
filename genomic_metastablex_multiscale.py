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


def extract_features(seq, window):
    feats = []
    for i in range(0, len(seq)-window, window):
        w = seq[i:i+window]
        feats.append([
            gc(w),
            entropy(w),
            len(set(w))/len(w)
        ])
    return np.array(feats)


# =========================
# MULTI-SCALE PCA
# =========================
def multiscale_signal(seq, windows):

    signals = []

    for w in windows:
        X = extract_features(seq, w)
        X = StandardScaler().fit_transform(X)

        pca = PCA(n_components=1)
        s = pca.fit_transform(X).flatten()

        # interpolar para tamanho máximo
        s_interp = np.interp(
            np.linspace(0, len(s), num=2000),
            np.arange(len(s)),
            s
        )

        signals.append(s_interp)

    return np.mean(signals, axis=0)


# =========================
# MAIN
# =========================
def main(args):

    os.makedirs("plots", exist_ok=True)

    seq = load_fasta(args.fasta)

    print("🧬 multiscale...")

    signal = multiscale_signal(seq, [500,1500,3000,6000])

    # 🔥 smoothing pesado (agora faz sentido)
    smooth = gaussian_filter1d(signal, sigma=20)

    smooth = (smooth - smooth.min())/(smooth.max()-smooth.min())

    # 🔥 domínios reais
    km = KMeans(n_clusters=3, random_state=42)
    domain = km.fit_predict(smooth.reshape(-1,1))

    # 🔥 risco real
    risk = np.abs(np.gradient(smooth))
    risk = gaussian_filter1d(risk, sigma=5)
    risk = risk / np.max(risk)

    # =========================
    # PCA VISUAL
    # =========================
    X = extract_features(seq, 3000)
    X = StandardScaler().fit_transform(X)
    P = PCA(n_components=2).fit_transform(X)

    # =========================
    # PLOTS
    # =========================
    x = np.arange(len(smooth))

    plt.figure(figsize=(6,6))
    plt.scatter(P[:,0], P[:,1], s=5)
    plt.gca().set_aspect('equal', adjustable='box')
    plt.savefig("plots/pca.png", dpi=300)
    plt.close()

    plt.figure()
    plt.plot(x, smooth)
    plt.title("Structural Axis (multiscale)")
    plt.savefig("plots/structure.png", dpi=300)
    plt.close()

    plt.figure()
    plt.plot(x, risk)
    plt.title("Metastable Risk")
    plt.savefig("plots/risk.png", dpi=300)
    plt.close()

    fig, axs = plt.subplots(3,1, figsize=(8,8), sharex=True)

    axs[0].scatter(P[:,0], P[:,1], s=5)
    axs[0].set_title("A) Structural Manifold")
    axs[0].set_aspect('equal')

    axs[1].plot(x, smooth)
    axs[1].set_title("B) Structural Axis")

    axs[2].plot(x, risk)
    axs[2].set_title("C) Metastable Risk")

    plt.tight_layout()
    plt.savefig("plots/paper.png", dpi=300)

    print("🔥 MULTISCALE DONE")


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--fasta", required=True)
    args = parser.parse_args()

    main(args)

