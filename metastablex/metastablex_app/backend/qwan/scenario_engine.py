SCENARIOS = {}

def save_scenario(name, H, I, Phi):
    if name not in SCENARIOS:
        SCENARIOS[name] = []

    SCENARIOS[name].append((H, I, Phi))

def compare():
    summary = {}
    for name, data in SCENARIOS.items():
        if not data:
            continue
        H = sum(x[0] for x in data)/len(data)
        I = sum(x[1] for x in data)/len(data)
        Phi = sum(x[2] for x in data)/len(data)

        summary[name] = {
            "H": H,
            "I": I,
            "Phi": Phi
        }

    return summary
