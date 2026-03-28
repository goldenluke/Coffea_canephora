import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage import laplace
import imageio.v2 as imageio

from metastablex.qwan.dynamics import evolve

# =========================
# CONFIG (AJUSTE CONFORME SUA MÁQUINA)
# =========================
N = 64
FRAMES = 5000        # 🔥 aumente para 10000+ se quiser
FPS = 60             # suavidade
OUT = "qwan_max.mp4"

ALPHA = 2.0          # separação de fase
BETA  = 3.0          # tensão superficial
GAMMA = 1.0          # potencial

# =========================
# INIT
# =========================
field = np.random.uniform(-0.1, 0.1, (N, N))
x = torch.tensor(field.flatten(), dtype=torch.float32)

H_series = []
I_series = []
Phi_series = []

# =========================
# FIGURA REUTILIZÁVEL (SEM RECRIAR → PERFORMANCE)
# =========================
fig = plt.figure(figsize=(10,6), facecolor='black')
grid = plt.GridSpec(2,2)

ax1 = fig.add_subplot(grid[:,0])
ax2 = fig.add_subplot(grid[0,1])
ax3 = fig.add_subplot(grid[1,1])

for ax in (ax1, ax2, ax3):
    ax.set_facecolor("black")
    ax.tick_params(colors='white')

ax1.axis("off")

print("Renderizando direto para vídeo...")

# =========================
# WRITER (STREAM → SEM PNG)
# =========================
with imageio.get_writer(OUT, fps=FPS, codec='libx264') as writer:

    for step in range(FRAMES):

        # -------------------------
        # MetastableX (global)
        # -------------------------
        x, history = evolve(
            x,
            steps=3,
            k=0.6,
            sigma=0.03
        )

        field = x.detach().numpy().reshape(N, N)

        # -------------------------
        # Física de campo (bolha)
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

        # volta para tensor
        x = torch.tensor(field.flatten(), dtype=torch.float32)

        # -------------------------
        # MÉTRICAS
        # -------------------------
        h = history[-1]
        H_series.append(h["H"])
        I_series.append(h["I"])
        Phi_series.append(h["Phi"])

        # =========================
        # ATUALIZA FIGURA (sem recriar)
        # =========================
        ax1.clear(); ax2.clear(); ax3.clear()

        # estilos novamente após clear
        ax1.set_facecolor("black")
        ax2.set_facecolor("black")
        ax3.set_facecolor("black")

        ax2.tick_params(colors='white')
        ax3.tick_params(colors='white')

        # -------- campo --------
        ax1.axis("off")
        img = (field - field.min()) / (field.max() - field.min() + 1e-8)
        ax1.imshow(img, cmap='magma')
        ax1.set_title(f"QWAN Field | step={step}", color='white')

        # -------- métricas --------
        ax2.plot(Phi_series, 'w-', label="Φ")
        ax2.plot(H_series, 'c--', label="H")
        ax2.plot(I_series, 'y--', label="I")
        ax2.set_title("Dynamics", color='white')

        leg = ax2.legend(facecolor='black', edgecolor='white')
        for t in leg.get_texts():
            t.set_color("white")

        # -------- energia --------
        ax3.plot(Phi_series, 'm-', label="Energy")
        ax3.set_title("Energy Evolution", color='white')

        leg2 = ax3.legend(facecolor='black', edgecolor='white')
        for t in leg2.get_texts():
            t.set_color("white")

        # =========================
        # RENDER → ARRAY (FIX MATPLOTLIB NOVO)
        # =========================
        fig.canvas.draw()
        image = np.asarray(fig.canvas.buffer_rgba())[:, :, :3]

        writer.append_data(image)

        if step % 200 == 0:
            print(f"{step}/{FRAMES}")

print("Vídeo final:", OUT)
