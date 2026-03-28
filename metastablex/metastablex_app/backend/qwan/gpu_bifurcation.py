import torch
import numpy as np
import matplotlib.pyplot as plt

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def simulate_batch(k_vals, noise_vals, steps=80, size=32):

    results = np.zeros((len(k_vals), len(noise_vals)))

    for i,k in enumerate(k_vals):
        for j,n in enumerate(noise_vals):

            field = torch.randn(size, size, device=device)*0.1

            for _ in range(steps):

                lap = (
                    -4*field
                    + torch.roll(field,1,0)
                    + torch.roll(field,-1,0)
                    + torch.roll(field,1,1)
                    + torch.roll(field,-1,1)
                )

                dG = field*(field**2 - 1)
                field = field + 0.05*(-k*dG + 3*lap + n*torch.randn_like(field))
                field = torch.clamp(field, -2, 2)

            results[i,j] = torch.mean(field**2).item()

    return results

def generate():

    k_vals = np.linspace(1,4,30)
    noise_vals = np.linspace(0,0.05,30)

    Z = simulate_batch(k_vals, noise_vals)

    plt.imshow(Z, origin="lower", aspect="auto", cmap="inferno")
    plt.colorbar(label="Phi")
    plt.xlabel("noise")
    plt.ylabel("k")
    plt.title("GPU Bifurcation Map")

    plt.savefig("gpu_bifurcation.png")
    plt.close()

    return "gpu_bifurcation.png"
