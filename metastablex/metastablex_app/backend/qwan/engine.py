import numpy as np
from scipy.ndimage import laplace

# tentativa de importar MetastableX
try:
    from metastablex.qwan.dynamics import evolve
    USE_META = True
    print("MetastableX carregado")
except:
    USE_META = False
    print("Fallback ativado")

def run_simulation(steps=50, size=32):

    field = np.random.uniform(-0.1, 0.1, (size, size))

    history = []

    for step in range(steps):

        if USE_META:
            import torch
            x = torch.tensor(field.flatten(), dtype=torch.float32)
            x, hist = evolve(x, steps=1)
            field = x.detach().numpy().reshape(size, size)

            h = hist[-1]
            H = float(h.get("H", 0))
            I = float(h.get("I", 0))
            Phi = float(h.get("Phi", 0))
        else:
            # fallback físico
            lap = laplace(field)
            field = field + 0.1 * lap

            H = float(np.mean(field))
            I = float(np.var(field))
            Phi = float(np.mean(field**2))

        history.append({
            "field": field.tolist(),
            "H": H,
            "I": I,
            "Phi": Phi
        })

    print("Simulação OK:", len(history))

    return history
