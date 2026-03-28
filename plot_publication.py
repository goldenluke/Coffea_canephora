import numpy as np
import matplotlib.pyplot as plt

def plot_publication(P, real_s, real_r, shuf_r):

    fig = plt.figure(figsize=(10,12))

    # =========================
    # A — PCA
    # =========================
    ax1 = plt.subplot(4,1,1)
    sc = ax1.scatter(P[:,0], P[:,1], c=P[:,0], s=6)
    ax1.set_title("A) Structural Manifold", fontsize=12, fontweight="bold")
    ax1.set_xticks([])
    ax1.set_yticks([])

    # =========================
    # B — STRUCTURAL AXIS
    # =========================
    ax2 = plt.subplot(4,1,2)
    ax2.plot(real_s, linewidth=1)
    ax2.set_title("B) Structural Axis", fontsize=12, fontweight="bold")
    ax2.set_ylabel("Normalized signal")

    # =========================
    # C — RISK COMPARISON
    # =========================
    ax3 = plt.subplot(4,1,3)
    ax3.plot(real_r, label="Real", linewidth=1.2)
    ax3.plot(shuf_r, label="Shuffled", alpha=0.7, linewidth=1)
    ax3.legend(frameon=False)
    ax3.set_title("C) Metastable Risk", fontsize=12, fontweight="bold")

    # =========================
    # D — DISTRIBUTION
    # =========================
    ax4 = plt.subplot(4,1,4)
    ax4.hist(real_r, bins=50, alpha=0.7, label="Real")
    ax4.hist(shuf_r, bins=50, alpha=0.5, label="Shuffled")
    ax4.legend(frameon=False)
    ax4.set_title("D) Risk Distribution", fontsize=12, fontweight="bold")

    plt.tight_layout()
    plt.savefig("plots/figure_1_publication.png", dpi=300)
    plt.savefig("plots/figure_1_publication.pdf")

    print("📊 figure saved: plots/figure_1_publication.(png/pdf)")


# =========================
# FIGURA 2 — DELTA
# =========================
def plot_delta(real_r, shuf_r):

    delta = real_r - shuf_r

    plt.figure(figsize=(10,4))
    plt.plot(delta, linewidth=1)
    plt.axhline(0, linestyle="--")
    plt.title("Difference (Real - Shuffled)", fontweight="bold")
    plt.ylabel("Δ Risk")

    plt.tight_layout()
    plt.savefig("plots/figure_2_delta.png", dpi=300)
    plt.savefig("plots/figure_2_delta.pdf")

    print("📊 delta figure saved")


