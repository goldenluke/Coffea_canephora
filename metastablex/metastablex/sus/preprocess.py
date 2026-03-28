import pandas as pd

def preprocess_sih():

    df = pd.read_parquet("data/sih_to.parquet")

    # município
    df["municipio"] = df["MUNIC_RES"]

    # ano-mês
    df["data"] = pd.to_datetime(df["ANO_CMPT"].astype(str) + "-" + df["MES_CMPT"].astype(str))

    # agregação
    agg = (
        df.groupby(["municipio", "data"])
        .size()
        .reset_index(name="internacoes")
    )

    agg.to_csv("data/sih_agg.csv", index=False)

    return agg
