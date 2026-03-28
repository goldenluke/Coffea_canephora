import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

def plot_nature(P, real_s, real_r, shuf_r):

    plt.figure(figsize=(10,10))

    # =========================
    # A — PCA (MAIOR)
    # =========================
    ax1 = plt.subplot2grid((4,1),(0,0), rowspan=1)
    sc = ax1.scatter(P[:,0], P[:,1], c=P[:,0], s=6)
    ax1.set_title("A) Structural Manifold", fontweight="bold")
    ax1.set_xticks([])
    ax1.set_yticks([])

    cbar = plt.colorbar(sc, ax=ax1)
    cbar.set_label("PC1")

    # =========================
    # B — STRUCTURE
    # =========================
    ax2 = plt.subplot2grid((4,1),(1,0))
    ax2.plot(real_s, linewidth=1)
    ax2.set_title("B) Structural Axis", fontweight="bold")
    ax2.set_ylabel("Normalized")

    # =========================
    # C — RISK
    # =========================
    ax3 = plt.subplot2grid((4,1),(2,0))
    ax3.plot(real_r, label="Real", linewidth=1.2)
    ax3.plot(shuf_r, label="Shuffled", alpha=0.6)
    ax3.legend(frameon=False)
    ax3.set_title("C) Metastable Risk", fontweight="bold")

    # =========================
    # D — DISTRIBUTION (KDE 🔥)
    # =========================
    ax4 = plt.subplot2grid((4,1),(3,0))
    sns.kdeplot(real_r, label="Real", fill=True, alpha=0.4)
    sns.kdeplot(shuf_r, label="Shuffled", fill=True, alpha=0.3)
    ax4.legend(frameon=False)
    ax4.set_title("D) Risk Distribution", fontweight="bold")

    plt.tight_layout()

    plt.savefig("plots/figure_nature_final.png", dpi=300)
    plt.savefig("plots/figure_nature_final.pdf")

    print("🔥 figure saved: plots/figure_nature_final")

