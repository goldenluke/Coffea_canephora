import torch
import pandas as pd
import os

SCENARIOS = {
    "low_noise": {"k": 2.0, "noise": 0.005},
    "critical": {"k": 2.5, "noise": 0.02},
    "chaotic": {"k": 3.5, "noise": 0.04},
}

def run_scenario(name, params, steps=300, size=32):

    field = torch.randn(size, size)*0.1
    data = []

    for _ in range(steps):

        lap = (
            -4*field
            + torch.roll(field,1,0)
            + torch.roll(field,-1,0)
            + torch.roll(field,1,1)
            + torch.roll(field,-1,1)
        )

        dG = field*(field**2 - 1)
        field = field + 0.05*(-params["k"]*dG + 3*lap + params["noise"]*torch.randn_like(field))
        field = torch.clamp(field, -2, 2)

        H = torch.mean(field).item()
        I = torch.var(field).item()
        Phi = torch.mean(field**2).item()

        data.append([H,I,Phi])

    df = pd.DataFrame(data, columns=["H","I","Phi"])
    path = f"dataset_{name}.csv"
    df.to_csv(path, index=False)

    return path

def generate_all():
    paths = []
    for name, params in SCENARIOS.items():
        print(f"Running {name}")
        paths.append(run_scenario(name, params))
    return paths
