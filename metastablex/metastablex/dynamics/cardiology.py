import numpy as np

def simulate_hrv(n=1500, regime="healthy", seed=42):
    """
    Simula série de Heart Rate Variability.

    Regimes disponíveis:
    - healthy
    - rigid
    - chaotic
    """

    np.random.seed(seed)

    hr = np.zeros(n)
    hr[0] = 70

    sympathetic = 0
    parasympathetic = 0

    for t in range(1, n):

        sympathetic = 0.95 * sympathetic + np.random.normal(0, 0.5)
        parasympathetic = 0.95 * parasympathetic + np.random.normal(0, 0.5)

        balance = sympathetic - parasympathetic

        if regime == "healthy":
            alpha = 0.6
            beta = 0.4
            noise = 0.05

        elif regime == "rigid":
            alpha = 0.9
            beta = 0.05
            noise = 0.005

        elif regime == "chaotic":
            alpha = 0.2
            beta = 0.8
            noise = 0.2

        else:
            alpha = 0.6
            beta = 0.4
            noise = 0.05

        dhr = (
            -alpha * (hr[t-1] - 70)
            + beta * balance
            + noise * np.random.randn()
        )

        hr[t] = hr[t-1] + dhr

    rr = 60 / hr

    return rr
