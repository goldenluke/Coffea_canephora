import torch
from .field import QWANField
from .dynamics import evolve
from .neural_operator import NeuralOperator

def classify_regime(history):
    last = history[-1]

    if last["I"] > 1.0:
        return "CHAOTIC"
    elif last["I"] > 0.5:
        return "CRITICAL"
    else:
        return "METASTABLE"


def compute_risk(history):
    return history[-1]["I"]


def run_qwan(series, device="cpu"):
    field = QWANField(series)

    model = NeuralOperator().to(device)

    x_final, history = evolve(
        field.x,
        model=model,
        device=device
    )

    regime = classify_regime(history)
    risk = compute_risk(history)

    return {
        "final": x_final,
        "history": history,
        "regime": regime,
        "risk": risk
    }
