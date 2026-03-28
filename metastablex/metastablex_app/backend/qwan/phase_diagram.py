import matplotlib.pyplot as plt
import pandas as pd

def generate_phase():

    df = pd.read_csv("paper_dataset.csv")

    plt.figure()
    plt.scatter(df["H"], df["I"], c=df["Phi"], cmap="viridis")
    plt.xlabel("H")
    plt.ylabel("I")
    plt.title("Phase Diagram")

    plt.savefig("phase_diagram.png")
    plt.close()

    return "phase_diagram.png"
