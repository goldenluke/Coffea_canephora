import pandas as pd
from pysus.ftp.databases.sih import SIH

from metastablex.utils.population import load_population, merge_population, normalize_rate

def run_pipeline():
    print("🚀 PIPELINE SIH + POPULAÇÃO")

    sih = SIH().load()

    dfs = []

    for ano in [2019, 2020, 2021, 2022, 2023]:
        print(f"📅 {ano}")

        files = sih.get_files("RD", uf="TO", year=ano)

        parquet = sih.download(files)

        if hasattr(parquet, "to_dataframe"):
            df = parquet.to_dataframe()
        else:
            df = pd.concat([p.to_dataframe() for p in parquet])

        df["cod_mun_ibge_6"] = df["MUNIC_RES"].astype(str).str.zfill(6)

        agg = df.groupby(["cod_mun_ibge_6", "ANO_CMPT", "MES_CMPT"]).size().reset_index(name="internacoes")

        agg.rename(columns={"ANO_CMPT": "ano", "MES_CMPT": "mes"}, inplace=True)

        dfs.append(agg)

    df_sih = pd.concat(dfs)

    # =========================
    # POPULAÇÃO
    # =========================
    df_pop = load_population("populacao_estimada_completa_spline.csv")

    df = merge_population(df_sih, df_pop)

    # =========================
    # NORMALIZAÇÃO
    # =========================
    df = normalize_rate(df)

    # =========================
    # DATA
    # =========================
    df["data"] = pd.to_datetime(df["ano"].astype(str) + "-" + df["mes"].astype(str) + "-01")

    # =========================
    # SALVAR
    # =========================
    df.to_csv("data/timeseries_to.csv", index=False)

    print("✅ pronto!")

if __name__ == "__main__":
    run_pipeline()
