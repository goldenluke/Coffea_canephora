import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

def plot_phase(embedded):

    if embedded is None:
        return None

    plt.figure()

    if embedded.shape[1] == 2:
        plt.plot(embedded[:,0], embedded[:,1])
        plt.xlabel("x(t)")
        plt.ylabel("x(t+τ)")

    elif embedded.shape[1] >= 3:
        ax = plt.axes(projection='3d')
        ax.plot3D(embedded[:,0], embedded[:,1], embedded[:,2])
        ax.set_xlabel("x")
        ax.set_ylabel("y")
        ax.set_zlabel("z")

    plt.title("Phase Space Reconstruction")
    plt.savefig("phase_reconstruction.png")
    plt.close()

    return "phase_reconstruction.png"
