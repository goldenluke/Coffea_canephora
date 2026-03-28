import streamlit as st
import pandas as pd
import numpy as np
import sys, os, time, requests

# =========================
# 🔧 PATH
# =========================
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, BASE_DIR)
sys.path.insert(0, os.path.join(BASE_DIR, "metastablex"))

# =========================
# 📦 IMPORTS
# =========================
from metastablex.core.data_loader import load_population
from metastablex.core.interpretation import *
from metastablex.core.hmm_model import fit_hmm
from metastablex.core.energy import energia_livre
from metastablex.core.critical import detectar_ruptura, sinais_criticos
from metastablex.core.entropy import entropia_rolling

# DATASUS + EPIDEMIOLOGIA
from metastablex.data.datasus_loader import load_sih_data
from metastablex.epidemiology.covid_detection import filtrar_covid
from metastablex.epidemiology.sir_model import rodar_sir

# =========================
# 🧠 LLM
# =========================
def explicar(contexto):
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": f"Responda em português:\n{contexto}",
                "stream": False,
                "options": {"num_predict": 300}
            },
            timeout=180
        )
        data = r.json()

        if "response" in data:
            return data["response"]

        if "message" in data:
            return data["message"].get("content", str(data))

        return str(data)

    except Exception as e:
        return f"Erro no LLM: {e}"

# =========================
# 🎛 CONFIG
# =========================
st.set_page_config(layout="wide")
st.title("🧠 MetastableX — Vigilância Epidemiológica")

# =========================
# 📥 DADOS BASE
# =========================
df_pop, _ = load_population()
df = df_pop.copy()

# =========================
# 🔥 SIMULAÇÃO COM PANDEMIA
# =========================
df["valor"] = np.random.poisson(50, len(df))

# pandemia simulada
df.loc[df["ano"].between(2020, 2021), "valor"] *= 4

# =========================
# 🧬 CID (simulado)
# =========================
df["cid"] = np.random.choice(
    ["U07.1", "J45", "E11", "I10", "A15"],
    size=len(df)
)

# normalização
df["taxa_por_100k"] = (df["valor"] / df["populacao"]) * 100000

# =========================
# 🎛 FILTROS
# =========================
st.sidebar.header("Filtros")

ufs = st.sidebar.multiselect("UF", df["UF"].unique(), default=[df["UF"].unique()[0]])

anos = st.sidebar.slider(
    "Ano",
    int(df["ano"].min()),
    int(df["ano"].max()),
    (2015, 2023)
)

# CID
cid_input = st.sidebar.text_input("CID (prefixo, ex: U07)")
cid_multi = st.sidebar.multiselect("Selecionar CID", df["cid"].unique())

df = df[
    (df["UF"].isin(ufs)) &
    (df["ano"].between(*anos))
]

# aplicar CID
if cid_input:
    df = df[df["cid"].str.upper().str.startswith(cid_input.upper())]
elif cid_multi:
    df = df[df["cid"].isin(cid_multi)]

# municípios
municipios = st.sidebar.multiselect(
    "Municípios",
    df["municipio"].unique(),
    default=list(df["municipio"].unique())[:3]
)

df = df[df["municipio"].isin(municipios)]

# =========================
# 📊 COMPARAÇÃO
# =========================
st.header("📊 Série Temporal")

pivot = df.pivot_table(index="ano", columns="municipio", values="taxa_por_100k")
st.line_chart(pivot)

# =========================
# 🧠 ANÁLISE
# =========================
st.header("🧠 Análise")

resultados = []

for mun in municipios:
    sub = df[df["municipio"] == mun].sort_values("ano")
    serie = sub["taxa_por_100k"]

    if len(serie) < 5:
        continue

    resultados.append({
        "municipio": mun,
        "tendencia": interpretar_tendencia(serie),
        "volatilidade": interpretar_volatilidade(serie),
        "alerta": detectar_ruptura(serie)
    })

df_result = pd.DataFrame(resultados)

if df_result.empty:
    st.warning("Sem dados suficientes")
else:
    st.dataframe(df_result)

# =========================
# 🚨 SURTOS
# =========================
st.header("🚨 Surtos")

if not df_result.empty:
    surtos = df_result[df_result["alerta"] == "ALTO RISCO"]

    if not surtos.empty:
        st.error("SURTO DETECTADO")
        st.write(surtos)
    else:
        st.success("Sem surtos críticos")

# =========================
# 🏆 RANKING POR CID
# =========================
st.header("🏆 Ranking por CID")

ranking = (
    df.groupby(["municipio", "UF"])["taxa_por_100k"]
    .mean()
    .reset_index()
    .sort_values(by="taxa_por_100k", ascending=False)
)

top_n = st.slider("Top N", 5, 30, 10)
top_ranking = ranking.head(top_n)

st.dataframe(top_ranking)
st.bar_chart(top_ranking.set_index("municipio")["taxa_por_100k"])

# =========================
# 🔬 ANÁLISE AVANÇADA
# =========================
st.header("🔬 Física Estatística")

if municipios:
    mun_sel = st.selectbox("Município", municipios)

    sub = df[df["municipio"] == mun_sel].sort_values("ano")
    serie = sub["taxa_por_100k"]

    if len(serie) > 5:
        states, _ = fit_hmm(serie)
        xs, energia = energia_livre(serie)
        ac, _ = sinais_criticos(serie)
        ent = entropia_rolling(serie)

        st.line_chart(serie)
        st.write("Estados HMM:", states)
        st.line_chart(pd.DataFrame({"energia": energia}, index=xs))
        st.line_chart(ac)
        st.line_chart(ent)

# =========================
# 🦠 DATASUS COVID REAL
# =========================
st.header("🦠 COVID (DATASUS)")

if st.button("Carregar COVID real"):
    with st.spinner("Baixando dados..."):

        df_sih = load_sih_data("SP", 2020)

        if not df_sih.empty:
            df_covid = filtrar_covid(df_sih)

            st.success(f"{len(df_covid)} casos encontrados")

            df_covid["data"] = pd.to_datetime(df_covid["DT_INTER"])

            serie = df_covid.groupby("data").size()
            st.line_chart(serie)

            # =========================
            # 📈 SIR
            # =========================
            st.subheader("Modelo SIR")

            t, S, I, R = rodar_sir(1_000_000, len(df_covid), 60)

            sir_df = pd.DataFrame({"S": S, "I": I, "R": R})
            st.line_chart(sir_df)

# =========================
# 🧠 IA
# =========================
st.header("🧠 IA")

def criar_logger():
    container = st.empty()
    logs = []

    def log(msg):
        logs.append(msg)
        container.markdown("\n".join(logs))

    return log

if st.button("Gerar análise IA"):

    log = criar_logger()

    with st.spinner("Rodando IA..."):
        log("Preparando dados")

        contexto = f"""
        CID: {cid_input if cid_input else cid_multi}
        Ranking: {top_ranking.to_dict()}
        """

        log("Chamando modelo")

        resposta = explicar(contexto)

        log("Finalizado")

    st.markdown(resposta)

# =========================
# 📄 RELATÓRIO
# =========================
st.header("📄 Relatório")

def gerar_relatorio(df):
    texto = "RELATÓRIO\n\n"
    for _, r in df.iterrows():
        texto += f"{r['municipio']} - {r['alerta']}\n"
    return texto

if not df_result.empty:
    relatorio = gerar_relatorio(df_result)

    st.download_button(
        "Baixar relatório",
        relatorio,
        file_name="relatorio.txt"
    )
