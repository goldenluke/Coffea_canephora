import numpy as np
import torch
import matplotlib.pyplot as plt

def simulate_lambda(k, noise, steps=80, size=32):

    field = torch.randn(size, size)*0.1

    ref = field.clone()
    pert = field.clone() + 1e-6*torch.randn_like(field)

    total = 0

    for _ in range(steps):

        def evolve(f):
            lap = (
                -4*f
                + torch.roll(f,1,0)
                + torch.roll(f,-1,0)
                + torch.roll(f,1,1)
                + torch.roll(f,-1,1)
            )
            dG = f*(f**2 - 1)
            return f + 0.05*(-k*dG + 3*lap + noise*torch.randn_like(f))

        ref = evolve(ref)
        pert = evolve(pert)

        d = torch.norm(pert - ref)

        if d.item() == 0:
            continue

        total += torch.log(d / 1e-6).item()

        direction = (pert - ref) / d
        pert = ref + 1e-6 * direction

    return total / steps

def generate_map():

    ks = np.linspace(1,4,25)
    ns = np.linspace(0,0.05,25)

    Z = np.zeros((len(ks), len(ns)))

    for i,k in enumerate(ks):
        for j,n in enumerate(ns):
            Z[i,j] = simulate_lambda(k,n)

    plt.imshow(Z, origin="lower", cmap="coolwarm")
    plt.colorbar(label="Lyapunov λ")
    plt.xlabel("noise")
    plt.ylabel("k")
    plt.title("Lyapunov Map")

    plt.savefig("lyapunov_map.png")
    plt.close()

    return "lyapunov_map.png"
