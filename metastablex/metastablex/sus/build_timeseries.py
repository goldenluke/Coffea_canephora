import pandas as pd

def build_timeseries():

    sih = pd.read_csv("data/sih_agg.csv")
    pop = pd.read_csv("populacao_estimada_completa_spline.csv", sep=";")

    pop_to = pop[pop["UF"] == "TO"]

    # merge por município + ano
    sih["ano"] = pd.to_datetime(sih["data"]).dt.year

    df = sih.merge(
        pop_to,
        left_on=["municipio", "ano"],
        right_on=["cod_mun_ibge_6", "ano"],
        how="left"
    )

    # taxa por 10k habitantes
    df["taxa"] = df["internacoes"] / df["populacao"] * 10000

    df.to_csv("data/timeseries_to.csv", index=False)

    return df
