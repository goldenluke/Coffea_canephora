import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_atlas3d(points):

    c = points[:,0]
    s = points[:,1]
    e = points[:,2]

    fig = plt.figure(figsize=(8,7))
    ax = fig.add_subplot(111, projection='3d')

    ax.scatter(c,s,e,alpha=0.5,s=10)

    ax.set_xlabel("Complexity")
    ax.set_ylabel("Stability")
    ax.set_zlabel("Energy Landscape")

    ax.set_title("MetastableX Universal Regime Atlas")

    plt.show()
