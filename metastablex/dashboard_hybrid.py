import streamlit as st
import pandas as pd
import numpy as np
import requests

from metastablex.sus.etl_sih import processar_dados
from metastablex.core.hmm_model import fit_hmm
from metastablex.core.entropy import entropia_rolling
from metastablex.core.critical import detectar_ruptura

# =========================
# CONFIG
# =========================
st.set_page_config(layout="wide")
st.title("🧠 MetastableX — Epidemiologia Computacional")

# =========================
# ESTADOS
# =========================
UFs_BR = [
    "AC","AL","AP","AM","BA","CE","DF","ES","GO","MA",
    "MT","MS","MG","PA","PB","PR","PE","PI","RJ","RN",
    "RS","RO","RR","SC","SP","SE","TO"
]

# =========================
# SIDEBAR
# =========================
st.sidebar.header("Filtros")

modo_to = st.sidebar.checkbox("📍 Focar Tocantins", True)

ufs = ["TO"] if modo_to else st.sidebar.multiselect("UFs", UFs_BR, default=["TO"])

anos_range = st.sidebar.slider("📅 Anos", 2000, 2025, (2015, 2022))
anos = list(range(anos_range[0], anos_range[1] + 1))

meses = st.sidebar.multiselect("Meses", list(range(1,13)), default=[12])

cid_input = st.sidebar.text_input("CID (U07, J18...)")
cid_filtro = [cid_input] if cid_input else None

# =========================
# ETL
# =========================
with st.spinner("Carregando dados..."):
    df = processar_dados(
        ufs=ufs,
        anos=anos,
        meses=meses,
        arquivo_populacao="metastablex/populacao_estimada_completa_spline.csv",
        cid_filtro=cid_filtro
    )

if df.empty:
    st.error("❌ Sem dados")
    st.stop()

# =========================
# GARANTIAS
# =========================
df["taxa"] = pd.to_numeric(df["taxa"], errors="coerce").fillna(0)
df["ano"] = pd.to_numeric(df["ano"], errors="coerce")

# =========================
# COVID
# =========================
if "cid" in df.columns:
    df["is_covid"] = df["cid"].astype(str).str.contains("U07|B34", na=False)
else:
    df["is_covid"] = False

# =========================
# SÉRIE TEMPORAL
# =========================
st.header("📊 Série Temporal")

pivot = df.pivot_table(
    index="ano",
    columns="municipio",
    values="taxa",
    aggfunc="mean"
).fillna(0)

if pivot.empty:
    st.warning("Sem série temporal")
    st.stop()

st.line_chart(pivot)

# =========================
# SINAL GLOBAL
# =========================
serie = pivot.mean(axis=1)

st.subheader("📈 Sinal médio")
st.line_chart(serie)

# =========================
# COVID
# =========================
st.header("🦠 COVID")

covid_series = df[df["is_covid"]].groupby("ano")["taxa"].mean()

if not covid_series.empty:
    st.line_chart(covid_series)
    st.success(f"Pico: {covid_series.idxmax()}")

# =========================
# HMM (CORRIGIDO)
# =========================
st.header("🧠 Estados Ocultos")

if len(serie) < 8:
    st.warning("Poucos dados → HMM desativado")
    estados = np.zeros(len(serie))

else:
    try:
        # 🔥 reduzir complexidade
        estados = fit_hmm(serie, n_states=2)
    except Exception as e:
        st.error(f"HMM erro: {e}")
        estados = np.zeros(len(serie))

df_hmm = pd.DataFrame(estados, index=serie.index, columns=["estado"])
st.line_chart(df_hmm)

# =========================
# ENTROPIA
# =========================
st.header("🌪 Entropia")

ent = entropia_rolling(serie)
ent.index = serie.index

st.line_chart(ent)

# =========================
# RUPTURA
# =========================
st.header("⚠️ Ruptura")

rupt = detectar_ruptura(serie)

if rupt:
    anos_ruptura = [serie.index[i] for i in rupt]
    st.error(f"Rupturas detectadas: {anos_ruptura}")
else:
    st.success("Sem ruptura")

# =========================
# SURTOS
# =========================
st.header("🚨 Surtos")

threshold = serie.mean() + 2 * serie.std()

surtos = serie[serie > threshold]

if not surtos.empty:
    st.error("Surtos detectados")
    st.write(surtos)
else:
    st.success("Sem surtos")

# =========================
# RANKING
# =========================
st.header("🏆 Ranking")

ranking = df.groupby("municipio")["taxa"].mean().sort_values(ascending=False).head(20)

st.dataframe(ranking)

# =========================
# LLM
# =========================
st.header("🧠 Interpretação (Llama)")

def explicar_llama(contexto):
    try:
        r = requests.post(
            "http://localhost:11434/api/generate",
            json={
                "model": "llama3",
                "prompt": contexto,
                "stream": False
            },
            timeout=60
        )
        return r.json()["response"]
    except Exception as e:
        return str(e)

if st.button("Gerar interpretação"):

    with st.spinner("Analisando..."):

        contexto = f"""
        Série epidemiológica: {serie.to_dict()}
        COVID: {covid_series.to_dict()}
        Entropia: {ent.to_dict()}

        Explique em português:
        tendências, risco e pandemia
        """

        resposta = explicar_llama(contexto)

        st.write(resposta)

# =========================
# FINAL
# =========================
st.success("Sistema estável 🚀")
