import matplotlib.pyplot as plt

def plot_phase_diagram(atlas):
    H = [a["H"] for a in atlas]
    I = [a["I"] for a in atlas]

    plt.figure()
    plt.scatter(H, I)

    plt.xlabel("Entropy (H)")
    plt.ylabel("Coherence (I)")
    plt.title("MetastableX Phase Diagram")

    plt.savefig("phase_diagram.png", dpi=300)

def plot_risk(atlas):
    risk = [a["H"]/(a["I"]+1e-6) for a in atlas]

    plt.figure()
    plt.hist(risk, bins=20)

    plt.title("Risk Distribution")
    plt.savefig("risk.png", dpi=300)

def plot_dynamics(history):
    H = [h["H"].mean().item() for h in history]
    I = [h["I"].mean().item() for h in history]

    plt.figure()
    plt.plot(H, label="Entropy")
    plt.plot(I, label="Coherence")

    plt.legend()
    plt.title("System Dynamics")

    plt.savefig("dynamics.png", dpi=300)
