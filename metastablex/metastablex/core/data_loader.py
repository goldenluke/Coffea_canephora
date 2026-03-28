import pandas as pd

def load_population():
    df = pd.read_csv(
        "populacao_estimada_completa_spline.csv",
        sep=";"
    )

    df["cod_mun_ibge_7"] = df["cod_mun_ibge_7"].astype(str)

    map_mun = (
        df.drop_duplicates("cod_mun_ibge_7")
        .set_index("cod_mun_ibge_7")["municipio"]
        .to_dict()
    )

    return df, map_mun
