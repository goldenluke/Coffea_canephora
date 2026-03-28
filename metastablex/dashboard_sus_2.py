import streamlit as st
import pandas as pd
import torch
import matplotlib.pyplot as plt

from metastablex.qwan.runner import run_qwan
from metastablex.qwan.data_batch import build_batch
from metastablex.qwan.batch_engine import evolve_batch
from metastablex.qwan.train import train_model
from metastablex.atlas.regime_atlas import build_atlas

# =========================
# CONFIG
# =========================
st.set_page_config(layout="wide")
st.title("MetastableX — SUS Digital Twin")

DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

# =========================
# LOAD DATA
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("data/timeseries_to.csv")

    # fallback nome município
    if "municipio" not in df.columns:
        if "cod_mun_ibge_6" in df.columns:
            df["municipio"] = df["cod_mun_ibge_6"].astype(str)
        else:
            df["municipio"] = "unknown"

    return df


@st.cache_data
def load_pop():
    df_pop = pd.read_csv(
        "populacao_estimada_completa_spline.csv",
        sep=";"
    )

    df_pop["cod_mun_ibge_6"] = df_pop["cod_mun_ibge_6"].astype(str)

    df_pop = df_pop.groupby("cod_mun_ibge_6").last().reset_index()

    return df_pop


df = load_data()
df_pop = load_pop()

# merge nomes reais
if "cod_mun_ibge_6" in df.columns:
    df["cod_mun_ibge_6"] = df["cod_mun_ibge_6"].astype(str)

    df = df.merge(
        df_pop[["cod_mun_ibge_6", "municipio"]],
        on="cod_mun_ibge_6",
        how="left",
        suffixes=("", "_real")
    )

    df["municipio"] = df["municipio_real"].fillna(df["municipio"])

# =========================
# SIDEBAR
# =========================
st.sidebar.header("Configuração")

municipios = sorted(df["municipio"].unique())
selected = st.sidebar.selectbox("Município", municipios)

steps = st.sidebar.slider("Steps dinâmica", 10, 200, 80)
k = st.sidebar.slider("Acoplamento ambiente", 0.0, 1.0, 0.3)
sigma = st.sidebar.slider("Ruído", 0.0, 0.1, 0.01)

train_flag = st.sidebar.button("Treinar modelo (GPU)")

# =========================
# TREINAMENTO GLOBAL
# =========================
@st.cache_resource
def get_model():
    return None

if train_flag:
    st.warning("Treinando modelo em GPU...")
    model = train_model(df, municipios, device=DEVICE)
    st.success("Modelo treinado!")
else:
    model = get_model()

# =========================
# SÉRIE TEMPORAL
# =========================
st.subheader("Série Temporal")

sub = df[df["municipio"] == selected]
series = sub["taxa"].values

st.line_chart(series)

# =========================
# QWAN ANÁLISE
# =========================
st.subheader("Análise Estrutural")

result = run_qwan(series, device=DEVICE)

regime = result["regime"]
risk = result["risk"]
history = result["history"]

col1, col2 = st.columns(2)

col1.metric("Regime", regime)
col2.metric("Risco", f"{risk:.3f}")

# =========================
# DINÂMICA
# =========================
st.subheader("Dinâmica")

df_dyn = pd.DataFrame(history)
st.line_chart(df_dyn)

# =========================
# EXPLICAÇÃO AUTOMÁTICA (MUNICÍPIO)
# =========================
st.subheader("Interpretação — Município")

if risk > 1.0:
    st.error(f"{selected} apresenta aumento de autocorrelação e variabilidade → possível perda de resiliência progressiva")
elif risk > 0.5:
    st.warning(f"{selected} está em regime metastável → próximo de transição crítica")
else:
    st.success(f"{selected} apresenta dinâmica estável")

# estilo médico
st.markdown("**Interpretação clínica:**")
if risk > 1.0:
    st.write("Sistema apresenta padrão compatível com perda de resiliência progressiva.")
elif risk > 0.5:
    st.write("Sistema em estado adaptativo sob estresse.")
else:
    st.write("Sistema com comportamento estável.")

# estilo paper
st.markdown("**Interpretação científica:**")
st.write(
    "A dinâmica observada sugere transição estrutural no espaço de estados, com aumento de autocorrelação e variância indicando critical slowing down."
)

# =========================
# RANKING GLOBAL
# =========================
st.subheader("Ranking de Risco")

ranking = {}

for mun in municipios:

    s = df[df["municipio"] == mun]["taxa"].values

    if len(s) < 20:
        continue

    res = run_qwan(s)

    ranking[mun] = res

ranking_df = build_atlas(ranking)
ranking_df = ranking_df.sort_values("I", ascending=False)

st.dataframe(ranking_df.head(20))

# =========================
# ATLAS 2D
# =========================
st.subheader("Atlas (Complexidade vs Estabilidade)")

fig, ax = plt.subplots()
ax.scatter(ranking_df["H"], ranking_df["I"])
ax.set_xlabel("Complexidade")
ax.set_ylabel("Estabilidade")

st.pyplot(fig)

# =========================
# ATLAS 3D
# =========================
st.subheader("Atlas 3D")

from mpl_toolkits.mplot3d import Axes3D

fig = plt.figure()
ax = fig.add_subplot(111, projection="3d")

ax.scatter(
    ranking_df["H"],
    ranking_df["I"],
    ranking_df["Phi"]
)

ax.set_xlabel("Complexidade")
ax.set_ylabel("Estabilidade")
ax.set_zlabel("Energia")

st.pyplot(fig)

# =========================
# ANÁLISE ESTADUAL
# =========================
st.subheader("Análise do Estado")

mean_risk = ranking_df["I"].mean()

if mean_risk > 1.0:
    st.error("Estado apresenta sinais estruturais de instabilidade sistêmica.")
elif mean_risk > 0.5:
    st.warning("Estado em regime metastável com risco de transição crítica.")
else:
    st.success("Estado com dinâmica estável.")

# =========================
# SIMULAÇÃO
# =========================
st.subheader("Simulação Dinâmica")

if st.button("Simular com ruído"):

    x = torch.tensor(series, dtype=torch.float32).to(DEVICE)

    x_final, hist = evolve_batch(
        x.unsqueeze(0),
        model=None,
        steps=steps,
        k=k,
        sigma=sigma
    )

    sim = [h for h in hist]

    st.line_chart(sim)
