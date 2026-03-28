import torch
import numpy as np

def build_batch(df, municipios, window=50, device="cpu"):
    batch = []

    for mun in municipios:
        s = df[df["municipio"] == mun]["taxa"].values

        if len(s) < window:
            continue

        s = s[-window:]

        batch.append(s)

    batch = np.array(batch)

    return torch.tensor(batch, dtype=torch.float32).to(device)
