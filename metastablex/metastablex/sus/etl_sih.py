import pandas as pd
from pysus.online_data.SIH import SIH
from metastablex.utils.population import filtrar_populacao


def processar_dados(ufs, anos, arquivo_populacao, meses=None, cid_filtro=None):

    dfs = []

    sih = SIH()
    sih.load()

    for uf in ufs:
        for ano in anos:
            for mes in meses:

                print(f"[INFO] {uf}-{ano}-{mes}")

                df_pop = filtrar_populacao(arquivo_populacao, uf, ano)

                if df_pop.empty:
                    continue

                df_pop["cod_ibge"] = df_pop["cod_mun_ibge_7"].astype(str).str[:6]

                try:
                    files = sih.get_files("RD", uf=uf, year=ano, month=mes)

                    if not files:
                        continue

                    parquet = sih.download(files)
                    df_sih = parquet.to_dataframe()

                except Exception as e:
                    print(f"[ERRO SIH] {e}")
                    continue

                if df_sih.empty:
                    continue

                # 🔥 CID CORRETO
                df_sih["cid"] = df_sih["DIAG_PRINC"].astype(str)

                # 🔥 filtro CID
                if cid_filtro:
                    df_sih = df_sih[
                        df_sih["cid"].str.contains("|".join(cid_filtro), na=False)
                    ]

                df_sih["cod_ibge"] = df_sih["MUNIC_RES"].astype(str).str.zfill(6)

                # 🔥 agregação COM CID
                agg = df_sih.groupby(["cod_ibge", "cid"]).size().reset_index(name="total")

                df = df_pop.merge(agg, on="cod_ibge", how="left")

                df["total"] = df["total"].fillna(0)
                df["cid"] = df["cid"].fillna("OUTROS")

                df["taxa"] = (df["total"] / df["populacao"]) * 100000
                df["ano"] = ano

                dfs.append(df)

    if not dfs:
        return pd.DataFrame()

    return pd.concat(dfs, ignore_index=True)
