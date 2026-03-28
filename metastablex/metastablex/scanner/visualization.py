import matplotlib.pyplot as plt

def plot_regime_map(points, labels):

    x = points[:,0]
    y = points[:,1]

    plt.figure(figsize=(8,6))

    plt.scatter(x,y,c=labels,cmap="viridis")

    plt.xlabel("Complexity Axis")

    plt.ylabel("Stability Axis")

    plt.title("Global Regime Map")

    plt.show()
