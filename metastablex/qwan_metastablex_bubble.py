import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from scipy.ndimage import laplace

from metastablex.qwan.dynamics import evolve

# =========================
# CONFIG
# =========================
N = 64
FRAMES = 120
OUT = "qwan_bubble.gif"

ALPHA = 2.0   # liberdade → separação
BETA  = 3.0   # coerência → tensão superficial
GAMMA = 1.0   # potencial

# =========================
# INIT CAMPO
# =========================
field = np.random.uniform(-0.1, 0.1, (N, N))
x = torch.tensor(field.flatten(), dtype=torch.float32)

states = []
H_series = []
I_series = []
Phi_series = []

# =========================
# EVOLUÇÃO HÍBRIDA
# =========================
for step in range(FRAMES):

    # -------------------------
    # 1. METASTABLEX (global)
    # -------------------------
    x, history = evolve(
        x,
        steps=3,
        k=0.6,
        sigma=0.03
    )

    field = x.detach().numpy().reshape(N, N)

    # -------------------------
    # 2. FÍSICA DE CAMPO (local)
    # -------------------------
    lap = laplace(field)

    # potencial duplo poço (CRUCIAL)
    dG = field * (field**2 - 1)

    # dinâmica tipo TDGL
    force = (
        -GAMMA * dG
        + ALPHA * (field - field.mean())
        + BETA * lap
    )

    field = field + 0.05 * force

    # normaliza
    field = np.clip(field, -2, 2)

    # volta pro tensor
    x = torch.tensor(field.flatten(), dtype=torch.float32)

    # -------------------------
    # salvar
    # -------------------------
    states.append(field.copy())

    h = history[-1]
    H_series.append(h["H"])
    I_series.append(h["I"])
    Phi_series.append(h["Phi"])

print("Simulação concluída.")

# =========================
# VISUAL
# =========================
fig = plt.figure(figsize=(12,6), facecolor='black')
grid = plt.GridSpec(2,2)

ax_main = fig.add_subplot(grid[:,0])
im = ax_main.imshow(states[0], cmap='magma')
ax_main.set_title("QWAN Bubble Formation", color='white')
ax_main.axis("off")

ax_metrics = fig.add_subplot(grid[0,1])
line_phi, = ax_metrics.plot([], [], 'w-', label="Φ")
line_h,   = ax_metrics.plot([], [], 'c--', label="H")
line_i,   = ax_metrics.plot([], [], 'y--', label="I")

ax_metrics.set_facecolor("black")
ax_metrics.tick_params(colors='white')
ax_metrics.legend(facecolor='black')

ax_env = fig.add_subplot(grid[1,1])
line_env, = ax_env.plot([], [], 'm-', label="Energy")

ax_env.set_facecolor("black")
ax_env.tick_params(colors='white')
ax_env.legend(facecolor='black')

def update(frame):

    data = states[frame]
    data = (data - data.min()) / (data.max() - data.min() + 1e-8)

    im.set_array(data)

    t = range(frame+1)

    line_phi.set_data(t, Phi_series[:frame+1])
    line_h.set_data(t, H_series[:frame+1])
    line_i.set_data(t, I_series[:frame+1])
    line_env.set_data(t, Phi_series[:frame+1])

    for ax in [ax_metrics, ax_env]:
        ax.relim()
        ax.autoscale_view()

    return im, line_phi, line_h, line_i, line_env

ani = FuncAnimation(fig, update, frames=FRAMES, interval=60, blit=True)

print("Renderizando...")
ani.save(OUT, writer="pillow", fps=20)

print("Pronto:", OUT)
