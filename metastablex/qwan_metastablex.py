import os
import numpy as np
import torch
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from metastablex.qwan.dynamics import evolve

# =========================
# CONFIG
# =========================
N = 64
FRAMES = 120
OUT = "qwan_metastablex.gif"

# =========================
# INIT
# =========================
field = np.random.randn(N, N)
x = torch.tensor(field.flatten(), dtype=torch.float32)

states = []
H_series = []
I_series = []
Phi_series = []

# =========================
# EVOLUÇÃO (DINÂMICA REAL)
# =========================
for step in range(FRAMES):

    x, history = evolve(
        x,
        steps=5,        # 🔥 aumenta dinâmica
        k=0.8,          # 🔥 acoplamento forte
        sigma=0.05      # 🔥 ruído maior
    )

    states.append(x.detach().numpy().reshape(N, N))

    h = history[-1]

    H_series.append(h["H"])
    I_series.append(h["I"])
    Phi_series.append(h["Phi"])

print("Simulação concluída.")

# =========================
# FIGURA
# =========================
fig = plt.figure(figsize=(12,6), facecolor='black')
grid = plt.GridSpec(2,2)

# =========================
# CAMPO
# =========================
ax_main = fig.add_subplot(grid[:,0])
im = ax_main.imshow(states[0], cmap='magma')
ax_main.set_title("MetastableX QWAN Field", color='white')
ax_main.axis("off")

# =========================
# MÉTRICAS
# =========================
ax_metrics = fig.add_subplot(grid[0,1])

line_phi, = ax_metrics.plot([], [], 'w-', label="Φ")
line_h,   = ax_metrics.plot([], [], 'c--', label="H")
line_i,   = ax_metrics.plot([], [], 'y--', label="I")

ax_metrics.set_facecolor("black")
ax_metrics.tick_params(colors='white')
ax_metrics.set_title("Dynamics", color='white')

legend = ax_metrics.legend(facecolor='black', edgecolor='white')
for text in legend.get_texts():
    text.set_color("white")

# =========================
# ENERGIA
# =========================
ax_env = fig.add_subplot(grid[1,1])

line_env, = ax_env.plot([], [], 'm-', label="Energy")

ax_env.set_facecolor("black")
ax_env.tick_params(colors='white')
ax_env.set_title("Energy Evolution", color='white')

legend2 = ax_env.legend(facecolor='black', edgecolor='white')
for text in legend2.get_texts():
    text.set_color("white")

# =========================
# UPDATE
# =========================
def update(frame):

    # normalização (evita parecer estático)
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

ani = FuncAnimation(
    fig,
    update,
    frames=FRAMES,
    interval=60,
    blit=True
)

print("Renderizando GIF...")
ani.save(OUT, writer="pillow", fps=20)

print("Pronto:", OUT)
