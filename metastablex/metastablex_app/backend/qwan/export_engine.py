import pandas as pd
import os

DATA = []

def add_row(H, I, Phi):
    DATA.append({"H": H, "I": I, "Phi": Phi})

def export_csv(path="qwan_dataset.csv"):
    df = pd.DataFrame(DATA)
    df.to_csv(path, index=False)
    return os.path.abspath(path)
