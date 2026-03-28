def merge_population(df_main, df_pop):
    df = df_main.merge(
        df_pop[["cod_mun_ibge_7", "ano", "populacao"]],
        on=["cod_mun_ibge_7", "ano"],
        how="left"
    )
    return df

def normalize(df):
    if "populacao" not in df.columns:
        if "populacao_x" in df.columns:
            df["populacao"] = df["populacao_x"]
        elif "populacao_y" in df.columns:
            df["populacao"] = df["populacao_y"]
        else:
            raise ValueError("populacao não encontrada")

    df["taxa_por_100k"] = (df["valor"] / df["populacao"]) * 100000
    return df
