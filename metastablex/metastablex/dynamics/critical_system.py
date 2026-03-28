import numpy as np

def simulate_critical_system(
    n=2000,
    dt=0.01,
    r=0.0,
    noise=0.02,
    x0=0.1
):
    """
    Simula sistema dinâmico próximo à criticidade.

    dx/dt = r*x - x^3 + noise

    r ≈ 0 -> criticidade
    r < 0 -> regime estável
    r > 0 -> regime instável
    """

    x = np.zeros(n)
    x[0] = x0

    for t in range(1, n):

        dx = (
            r * x[t-1]
            - x[t-1]**3
            + noise * np.random.randn()
        )

        x[t] = x[t-1] + dx * dt

    return x
