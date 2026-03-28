import numpy as np

def potential_landscape(returns, bins=30):
    hist, bins = np.histogram(returns, bins=bins, density=True)
    centers = (bins[:-1] + bins[1:]) / 2
    sigma = np.std(returns)
    U = -(sigma**2 / 2) * np.log(hist + 1e-12)
    return centers, U
