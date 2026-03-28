import matplotlib.pyplot as plt
import numpy as np

def plot_atlas(points):

    c = [p[0] for p in points]
    s = [p[1] for p in points]

    plt.figure(figsize=(7,7))

    plt.scatter(c,s,alpha=0.4,s=10)

    plt.xlabel("Complexity")
    plt.ylabel("Stability")

    plt.title("MetastableX Dynamic Regime Atlas")

    plt.show()
