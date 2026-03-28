import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

DATA = []

def add(H, I, Phi):
    DATA.append((H, I, Phi))

def export_all():

    df = pd.DataFrame(DATA, columns=["H","I","Phi"])

    # gráfico principal
    plt.figure()
    plt.plot(df["Phi"], label="Phi")
    plt.plot(df["H"], label="H")
    plt.plot(df["I"], label="I")
    plt.legend()
    plt.title("QWAN Dynamics")
    plt.savefig("paper_dynamics.png")
    plt.close()

    # scatter (fase)
    plt.figure()
    plt.scatter(df["H"], df["I"], c=df["Phi"], cmap="viridis")
    plt.xlabel("H")
    plt.ylabel("I")
    plt.title("Phase Space")
    plt.savefig("paper_phase.png")
    plt.close()

    df.to_csv("paper_dataset.csv", index=False)

    return {
        "csv": "paper_dataset.csv",
        "dynamics": "paper_dynamics.png",
        "phase": "paper_phase.png"
    }
