import pandas as pd
import glob

def compare():

    files = glob.glob("dataset_*.csv")
    results = []

    for f in files:
        df = pd.read_csv(f)

        results.append({
            "scenario": f,
            "H_mean": df["H"].mean(),
            "I_mean": df["I"].mean(),
            "Phi_mean": df["Phi"].mean()
        })

    out = pd.DataFrame(results)
    out.to_csv("comparison.csv", index=False)

    print(out)
    return "comparison.csv"
