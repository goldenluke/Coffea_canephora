import streamlit as st
import pandas as pd
import numpy as np
import torch

from metastablex.ml.train import train
from metastablex.ml.features import metastable_features

# =========================
# CONFIG
# =========================
st.set_page_config(layout="wide")
st.title("🧠 MetastableX — SIH Tocantins")
st.markdown("Ranking de risco e detecção de colapso hospitalar")

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("data/timeseries_to.csv")

    # 🔥 PADRONIZAÇÃO CRÍTICA
    df["municipio"] = df["municipio"].astype(str).str.zfill(6)
    df["data"] = pd.to_datetime(df["data"])

    return df

df = load_data()

# =========================
# LOAD MUNICIPIOS
# =========================
@st.cache_data
def load_municipios():
    pop = pd.read_csv("populacao_estimada_completa_spline.csv", sep=";")

    pop = pop[pop["UF"] == "TO"]

    pop["cod_mun_ibge_6"] = pop["cod_mun_ibge_6"].astype(str).str.zfill(6)

    return dict(zip(pop["cod_mun_ibge_6"], pop["municipio"]))

mapa_mun = load_municipios()

# =========================
# MAPEAR NOME
# =========================
df["nome"] = df["municipio"].map(mapa_mun)

# =========================
# SIDEBAR
# =========================
municipios_nome = sorted(df["nome"].dropna().unique())

selected_nome = st.sidebar.selectbox("Município", municipios_nome)

selected_cod = [k for k, v in mapa_mun.items() if v == selected_nome][0]

sub = df[df["municipio"] == selected_cod].sort_values("data")

# =========================
# SÉRIE
# =========================
st.subheader(f"📍 {selected_nome}")

col1, col2 = st.columns(2)

with col1:
    st.markdown("### 📈 Taxa de internações")
    st.line_chart(sub.set_index("data")["taxa"])

series = sub["taxa"].values.astype(float)

if len(series) < 10:
    st.warning("Série muito curta para análise")
    st.stop()

# =========================
# MODELO
# =========================
@st.cache_resource
def get_model(series_tuple):
    return train(np.array(series_tuple))

model = get_model(tuple(series))

features = metastable_features(series)

with torch.no_grad():
    preds = model(features).numpy()
    score = float(np.mean(preds))

# =========================
# MÉTRICAS
# =========================
var = float(np.var(series))

ac1 = float(np.corrcoef(series[1:], series[:-1])[0, 1]) if len(series) > 1 else 0

# entropia (robusta)
p = np.abs(series) + 1e-8
p = p / p.sum()
entropy = float(-np.sum(p * np.log(p)))

# =========================
# CLASSIFICAÇÃO
# =========================
if score > 0.66:
    regime = "🔴 CRÍTICO"
elif score > 0.5:
    regime = "🟡 METAESTÁVEL"
else:
    regime = "🟢 ESTÁVEL"

# =========================
# DISPLAY
# =========================
with col2:
    st.markdown("### 🧠 Diagnóstico")

    st.metric("Regime", regime)
    st.metric("Score", f"{score:.3f}")
    st.metric("Variância", f"{var:.2f}")

# =========================
# FEATURES VISUAIS
# =========================
st.markdown("### 🔬 Indicadores estruturais")

var_series = (series - np.mean(series)) ** 2

ac_series = np.zeros_like(series)
ac_series[1:] = series[1:] * series[:-1]

features_df = pd.DataFrame({
    "data": sub["data"],
    "variancia": var_series,
    "autocorrelacao": ac_series
})

st.line_chart(features_df.set_index("data"))

# =========================
# EARLY WARNING
# =========================
st.markdown("### ⚠️ Early Warning Signals")

col1, col2, col3 = st.columns(3)

col1.metric("Autocorrelação", f"{ac1:.3f}")
col2.metric("Entropia", f"{entropy:.3f}")
col3.metric("Variância", f"{var:.2f}")

if ac1 > 0.8:
    st.warning("⚠️ Critical slowing down detectado")

if var > np.percentile(series, 90):
    st.warning("⚠️ Alta variância (instabilidade crescente)")

# =========================
# RANKING
# =========================
st.markdown("---")
st.markdown("## 🏆 Ranking de risco")

@st.cache_data
def compute_ranking(df):

    results = []

    for m in df["municipio"].unique():

        sub = df[df["municipio"] == m].sort_values("data")
        series = sub["taxa"].values.astype(float)

        if len(series) < 10:
            continue

        try:
            feats = metastable_features(series)
            model = train(series)

            with torch.no_grad():
                score = float(model(feats).mean().item())

            results.append((m, score))

        except Exception as e:
            continue

    ranking = pd.DataFrame(results, columns=["municipio", "risco"])
    ranking["nome"] = ranking["municipio"].map(mapa_mun)

    return ranking.sort_values("risco", ascending=False)

ranking_df = compute_ranking(df)

st.dataframe(
    ranking_df[["nome", "risco"]].head(20),
    use_container_width=True
)

# =========================
# INTERPRETAÇÃO
# =========================
st.markdown("---")
st.markdown("## 🧠 Interpretação automática")

st.markdown(f"""
**{selected_nome} está em regime {regime}**

### 📊 Indicadores:
- Variância: {var:.2f}
- Autocorrelação: {ac1:.2f}
- Entropia: {entropy:.2f}

### 🧠 Interpretação:
- Alta variância → instabilidade crescente
- Alta autocorrelação → perda de resiliência
- Entropia elevada → exploração estrutural

### ⚠️ Implicação:
Possível aproximação de **colapso hospitalar**
""")
