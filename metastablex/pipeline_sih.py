# -*- coding: utf-8 -*-
import pandas as pd
import os
from pysus.online_data.SIH import SIH


UF = "TO"
ANOS = [2019, 2020, 2021, 2022, 2023]


def run_pipeline():

    print("\n🚀 PIPELINE SIH — TOCANTINS")

    os.makedirs("data", exist_ok=True)

    # =========================
    # LOAD SIH
    # =========================
    try:
        sih_db = SIH().load()
    except Exception as e:
        print(f"❌ Erro ao carregar SIH: {e}")
        return

    resultados = []

    # =========================
    # EXTRAÇÃO
    # =========================
    for ano in ANOS:

        print(f"\n📅 Ano {ano}")

        for mes in range(1, 13):

            print(f"  → Mês {mes:02d}")

            try:
                files = sih_db.get_files(
                    group="RD",
                    uf=UF,
                    year=ano,
                    month=mes
                )

                if not files:
                    continue

                parquet_set = sih_db.download(files)

                # 🔥 CORREÇÃO DO PARQUETSET
                if not hasattr(parquet_set, "to_dataframe"):
                    continue

                df_sih = parquet_set.to_dataframe()

            except Exception as e:
                print(f"⚠️ erro {ano}-{mes}: {e}")
                continue

            if df_sih.empty or "MUNIC_RES" not in df_sih.columns:
                continue

            # =========================
            # PROCESSAMENTO
            # =========================
            df_sih["municipio"] = df_sih["MUNIC_RES"].astype(str).str.zfill(6)

            df_sih["data"] = pd.to_datetime(f"{ano}-{mes:02d}")

            agg = (
                df_sih.groupby("municipio")
                .size()
                .reset_index(name="internacoes")
            )

            agg["data"] = df_sih["data"].iloc[0]

            resultados.append(agg)

    if not resultados:
        raise Exception("🚨 Nenhum dado processado")

    df_sih_final = pd.concat(resultados, ignore_index=True)

    print(f"\n📊 SIH linhas: {len(df_sih_final)}")

    # =========================
    # POPULAÇÃO
    # =========================
    print("\n📊 Integrando população...")

    pop_path1 = "populacao_estimada_completa_spline.csv"
    pop_path2 = "data/populacao_estimada_completa_spline.csv"

    if os.path.exists(pop_path1):
        pop = pd.read_csv(pop_path1, sep=";")
    elif os.path.exists(pop_path2):
        pop = pd.read_csv(pop_path2, sep=";")
    else:
        raise FileNotFoundError("Arquivo de população não encontrado")

    pop_to = pop[pop["UF"] == "TO"].copy()

    pop_to["cod_mun_ibge_6"] = pop_to["cod_mun_ibge_6"].astype(str)

    df_sih_final["ano"] = df_sih_final["data"].dt.year

    # 🔥 MERGE CORRIGIDO
    df = df_sih_final.merge(
        pop_to,
        left_on=["municipio", "ano"],
        right_on=["cod_mun_ibge_6", "ano"],
        how="left",
        suffixes=("", "_pop")
    )

    # =========================
    # TAXA
    # =========================
    df["taxa"] = df["internacoes"] / df["populacao"] * 10000

    # 🔥 GARANTIR COLUNA
    if "municipio" not in df.columns:
        if "municipio_x" in df.columns:
            df["municipio"] = df["municipio_x"]
        else:
            raise Exception("🚨 coluna municipio não encontrada")

    df = df[["municipio", "data", "taxa"]].dropna()

    # =========================
    # SALVAR
    # =========================
    output = "data/timeseries_to.csv"

    df.to_csv(output, index=False)

    print("\n✅ FINALIZADO")
    print(f"📁 {output}")
    print(f"📈 Total linhas: {len(df)}")


if __name__ == "__main__":
    run_pipeline()
