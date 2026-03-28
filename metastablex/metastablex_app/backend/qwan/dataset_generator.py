import torch
import pandas as pd

def generate_dataset(steps=300, size=32):

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
        field = field + 0.05*(-2*dG + 3*lap + 0.01*torch.randn_like(field))
        field = torch.clamp(field, -2, 2)

        H = torch.mean(field).item()
        I = torch.var(field).item()
        Phi = torch.mean(field**2).item()

        data.append([H, I, Phi])

    df = pd.DataFrame(data, columns=["H","I","Phi"])
    df.to_csv("paper_dataset.csv", index=False)

    print("Dataset gerado: paper_dataset.csv")
