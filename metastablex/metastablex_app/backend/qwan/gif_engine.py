import os
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.ndimage import laplace
import imageio.v2 as imageio

BASE_DIR = "/home/ld/metastablex/metastablex_app/backend"

try:
    import torch
    from metastablex.qwan.dynamics import evolve
    USE_META = True
except:
    USE_META = False

def generate_gif(steps=200, size=96):

    # 🔥 campo inicial (ruído leve)
    field = np.random.uniform(-0.1, 0.1, (size, size))

    frames = []
    Phi_series, H_series, I_series = [], [], []

    for step in range(steps):

        # -------------------------
        # METASTABLEX (driver global)
        # -------------------------
        if USE_META:
            x = torch.tensor(field.flatten(), dtype=torch.float32)
            x, hist = evolve(x, steps=2, k=0.6, sigma=0.01)
            field = x.detach().numpy().reshape(size, size)

            h = hist[-1]
            H = float(h.get("H", 0))
            I = float(h.get("I", 0))
            Phi = float(h.get("Phi", 0))
        else:
            H = float(np.mean(field))
            I = float(np.var(field))
            Phi = float(np.mean(field**2))

        # -------------------------
        # ANNEALING (temperatura ↓)
        # -------------------------
        T = max(0.03 * (1 - step / steps), 0.002)
        noise = np.random.randn(size, size) * T

        # -------------------------
        # FÍSICA DE FASE (NUCLEAÇÃO)
        # -------------------------
        lap = laplace(field)
        dG = field * (field**2 - 1)

        field = field + 0.04 * (
            -2.5 * dG      # separação de fase
            + 3.5 * lap    # tensão superficial
            + noise        # flutuação térmica
        )

        field = np.clip(field, -2, 2)

        # -------------------------
        # MÉTRICAS
        # -------------------------
        Phi_series.append(Phi)
        H_series.append(H)
        I_series.append(I)

        # -------------------------
        # FIGURA (paper-style)
        # -------------------------
        fig = plt.figure(figsize=(12,6), facecolor='black')
        grid = plt.GridSpec(2,2)

        # campo
        ax1 = fig.add_subplot(grid[:,0])
        img = (field - field.min())/(field.max()-field.min()+1e-8)
        ax1.imshow(img, cmap='inferno')
        ax1.set_title("QWAN Phase Nucleation", color='white')
        ax1.axis("off")

        # dinâmica
        ax2 = fig.add_subplot(grid[0,1])
        ax2.plot(Phi_series, 'w-', label="Φ")
        ax2.plot(H_series, 'c--', label="H")
        ax2.plot(I_series, 'y--', label="I")
        ax2.legend(facecolor='black')
        ax2.set_facecolor("black")
        ax2.tick_params(colors='white')

        # energia
        ax3 = fig.add_subplot(grid[1,1])
        ax3.plot(Phi_series, 'm-', label="Energy")
        ax3.legend(facecolor='black')
        ax3.set_facecolor("black")
        ax3.tick_params(colors='white')

        plt.tight_layout()

        fig.canvas.draw()
        frame = np.asarray(fig.canvas.buffer_rgba())[:,:,:3]
        frames.append(frame)

        plt.close()

    path = os.path.join(BASE_DIR, "qwan_paper.gif")
    imageio.mimsave(path, frames, fps=25)

    return path
