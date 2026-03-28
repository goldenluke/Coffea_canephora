import pandas as pd

def build_atlas(results):

    data = []

    for mun, res in results.items():

        last = res["history"][-1]

        data.append({
            "municipio": mun,
            "H": last["H"],
            "I": last["I"],
            "Phi": last["Phi"],
            "regime": res["regime"]
        })

    return pd.DataFrame(data)
