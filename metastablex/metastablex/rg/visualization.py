import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def plot_rg_flow(flow):

    C = flow[:,0]
    S = flow[:,1]
    E = flow[:,2]

    dC = flow[:,3]
    dS = flow[:,4]
    dE = flow[:,5]

    fig = plt.figure(figsize=(8,7))
    ax = fig.add_subplot(111, projection="3d")

    ax.quiver(
        C,S,E,
        dC,dS,dE,
        length=0.1,
        normalize=True
    )

    ax.set_xlabel("Complexity")
    ax.set_ylabel("Stability")
    ax.set_zlabel("Energy")

    ax.set_title("Regime RG Flow")

    plt.show()
