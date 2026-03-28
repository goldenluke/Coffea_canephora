import numpy as np

def synthetic_datasets():

    data = {}

    t = np.linspace(0,10,500)

    data["periodic"] = np.sin(t)

    data["chaotic"] = np.random.randn(500)

    data["trend"] = t + np.random.randn(500)

    data["critical"] = np.cumsum(np.random.randn(500))

    return data
