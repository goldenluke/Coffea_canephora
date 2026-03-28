# -*- coding: utf-8 -*-
import pandas as pd
from pysus.online_data.SIH import SIH
from metastablex.utils.population import filtrar_populacao
import logging

# 🔥 reduzir logs do pysus
logging.getLogger("pysus").setLevel(logging.ERROR)


def processar_dados(ufs, anos, arquivo_populacao, meses=None, cid_filtro=None):

    df_resultados = []

    try:
        sih_db = SIH()
        sih_db.load()  # ✅ NECESSÁRIO
    except Exception as e:
        print(f"❌ Erro ao carregar SIH: {e}")
        return pd.DataFrame()

    processar_por_mes = bool(meses) and len(meses) > 0

    for uf in ufs:
        for ano in anos:

            meses_iterar = meses if processar_por_mes else [None]

            for mes in meses_iterar:

                periodo = f"{uf}/{ano}" + (f"/{mes:02d}" if mes else " (anual)")
                print(f"\n=== {periodo} ===")

                df_base = filtrar_populacao(arquivo_populacao, uf, ano)

                if df_base is None or df_base.empty:
                    print("⚠️ População vazia")
                    continue

                try:
                    files = sih_db.get_files(group='RD', uf=uf, year=ano, month=mes)

                    if not files:
                        print("⚠️ Nenhum arquivo encontrado")
                        df_sih = pd.DataFrame()

                    else:
                        parquet_set = sih_db.download(files, local_dir="cache_sih")

                        if isinstance(parquet_set, list):
                            df_sih = pd.concat(
                                [p.to_dataframe() for p in parquet_set],
                                ignore_index=True
                            )
                        elif hasattr(parquet_set, "to_dataframe"):
                            df_sih = parquet_set.to_dataframe()
                        else:
                            df_sih = pd.DataFrame()

                except Exception as e:
                    print(f"❌ Erro SIH: {e}")
                    df_sih = pd.DataFrame()

                # =========================
                # SEM DADOS
                # =========================
                if df_sih.empty or 'MUNIC_RES' not in df_sih.columns:
                    df_base["total"] = 0
                    df_base["cid"] = "SEM_DADO"

                else:
                    # =========================
                    # CID
                    # =========================
                    df_sih["cid"] = df_sih["DIAG_PRINC"].astype(str)

                    if cid_filtro:
                        df_sih = df_sih[
                            df_sih["cid"].str.contains("|".join(cid_filtro), na=False)
                        ]

                    # =========================
                    # MUNICÍPIO
                    # =========================
                    df_sih["MUNIC_RES"] = df_sih["MUNIC_RES"].astype(str).str.zfill(6)

                    agg = df_sih.groupby(["MUNIC_RES", "cid"]).size().reset_index(name="total")

                    df_base["cod_ibge"] = df_base["cod_mun_ibge_7"].astype(str).str[:6]

                    df = df_base.merge(
                        agg,
                        left_on="cod_ibge",
                        right_on="MUNIC_RES",
                        how="left"
                    )

                    df["total"] = df["total"].fillna(0)
                    df["cid"] = df["cid"].fillna("OUTROS")

                    df_base = df

                # =========================
                # TAXA
                # =========================
                df_base["taxa"] = df_base.apply(
                    lambda r: (r["total"] / r["populacao"]) * 100000
                    if r["populacao"] > 0 else 0,
                    axis=1
                )

                df_base["ano"] = ano
                df_base["UF"] = uf

                df_resultados.append(df_base.reset_index(drop=True))

    if df_resultados:
        print("\n✅ Dados processados com sucesso")
        return pd.concat(df_resultados, ignore_index=True)

    print("\n⚠️ Nenhum dado processado")
    return pd.DataFrame()
