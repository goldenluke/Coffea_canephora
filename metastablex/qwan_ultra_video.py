import os
import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage import laplace
import imageio.v2 as imageio

from metastablex.qwan.dynamics import evolve

# =========================
# CONFIG
# =========================
N = 64
FRAMES = 800
OUT = "qwan_ultra.mp4"

ALPHA = 2.0
BETA  = 3.0
GAMMA = 1.0

os.makedirs("frames", exist_ok=True)

# =========================
# INIT
# =========================
field = np.random.uniform(-0.1, 0.1, (N, N))
x = torch.tensor(field.flatten(), dtype=torch.float32)

H_series = []
I_series = []
Phi_series = []

print("Gerando frames...")

# =========================
# LOOP PRINCIPAL
# =========================
for step in range(FRAMES):

    # -------------------------
    # MetastableX
    # -------------------------
    x, history = evolve(
        x,
        steps=3,
        k=0.6,
        sigma=0.03
    )

    field = x.detach().numpy().reshape(N, N)

    # -------------------------
    # Física (bolha)
    # -------------------------
    lap = laplace(field)
    dG = field * (field**2 - 1)

    force = (
        -GAMMA * dG
        + ALPHA * (field - field.mean())
        + BETA * lap
    )

    field = field + 0.05 * force
    field = np.clip(field, -2, 2)

    x = torch.tensor(field.flatten(), dtype=torch.float32)

    # -------------------------
    # MÉTRICAS
    # -------------------------
    h = history[-1]
    H_series.append(h["H"])
    I_series.append(h["I"])
    Phi_series.append(h["Phi"])

    # =========================
    # FIGURA COMPLETA
    # =========================
    fig = plt.figure(figsize=(10,6), facecolor='black')
    grid = plt.GridSpec(2,2)

    # CAMPO
    ax1 = fig.add_subplot(grid[:,0])
    img = (field - field.min()) / (field.max() - field.min() + 1e-8)
    ax1.imshow(img, cmap='magma')
    ax1.set_title(f"QWAN Field | step={step}", color='white')
    ax1.axis("off")

    # MÉTRICAS Φ H I
    ax2 = fig.add_subplot(grid[0,1])
    ax2.plot(Phi_series, 'w-', label="Φ")
    ax2.plot(H_series, 'c--', label="H")
    ax2.plot(I_series, 'y--', label="I")

    ax2.set_facecolor("black")
    ax2.tick_params(colors='white')
    ax2.set_title("Dynamics", color='white')

    legend = ax2.legend(facecolor='black', edgecolor='white')
    for text in legend.get_texts():
        text.set_color("white")

    # ENERGIA (Φ isolado)
    ax3 = fig.add_subplot(grid[1,1])
    ax3.plot(Phi_series, 'm-', label="Energy")

    ax3.set_facecolor("black")
    ax3.tick_params(colors='white')
    ax3.set_title("Energy Evolution", color='white')

    legend2 = ax3.legend(facecolor='black', edgecolor='white')
    for text in legend2.get_texts():
        text.set_color("white")

    plt.tight_layout()

    fname = f"frames/frame_{step:05d}.png"
    plt.savefig(fname, bbox_inches='tight', pad_inches=0)
    plt.close()

    if step % 50 == 0:
        print(f"Frame {step}/{FRAMES}")

print("Frames prontos.")

# =========================
# GERAR VÍDEO
# =========================
print("Renderizando vídeo...")

with imageio.get_writer(OUT, fps=30, codec='libx264') as writer:
    for i in range(FRAMES):
        fname = f"frames/frame_{i:05d}.png"
        image = imageio.imread(fname)
        writer.append_data(image)

print("Vídeo pronto:", OUT)
