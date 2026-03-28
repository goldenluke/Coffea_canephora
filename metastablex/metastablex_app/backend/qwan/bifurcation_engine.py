import numpy as np

def detect_bifurcation(history):
    if len(history) < 20:
        return False

    recent = np.array(history[-20:])
    std = np.std(recent)
    mean_shift = abs(np.mean(recent[:10]) - np.mean(recent[10:]))

    # bifurcação = aumento de variância + mudança média
    if std > 0.5 and mean_shift > 0.2:
        return True

    return False
