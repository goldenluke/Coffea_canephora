import numpy as np
import torch
import matplotlib.pyplot as plt

def simulate(k, noise, steps=100, size=32):

    field = torch.randn(size, size)*0.1

    for _ in range(steps):

        lap = (
            -4*field
            + torch.roll(field,1,0)
            + torch.roll(field,-1,0)
            + torch.roll(field,1,1)
            + torch.roll(field,-1,1)
        )

        dG = field*(field**2 - 1)
        field = field + 0.05*(-k*dG + 3*lap + noise*torch.randn_like(field))

    return torch.mean(field**2).item()

def generate_map():

    ks = np.linspace(0.5, 4, 20)
    noises = np.linspace(0, 0.05, 20)

    Z = np.zeros((len(ks), len(noises)))

    for i,k in enumerate(ks):
        for j,n in enumerate(noises):
            Z[i,j] = simulate(k,n)

    plt.imshow(Z, origin="lower", aspect="auto", cmap="inferno")
    plt.colorbar(label="Phi")
    plt.xlabel("noise")
    plt.ylabel("k")
    plt.title("Bifurcation Map")

    plt.savefig("bifurcation_map.png")
    plt.close()

    return "bifurcation_map.png"
