import matplotlib
matplotlib.use("Agg")

import matplotlib.pyplot as plt

def plot_multifractal(alpha, f_alpha):

    plt.figure()
    plt.plot(alpha, f_alpha)
    plt.xlabel("α")
    plt.ylabel("f(α)")
    plt.title("Multifractal Spectrum")

    plt.savefig("multifractal_spectrum.png")
    plt.close()

    return "multifractal_spectrum.png"
