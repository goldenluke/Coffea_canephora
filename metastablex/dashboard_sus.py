import streamlit as st
import pandas as pd
import torch
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

from metastablex.qwan.runner import run_qwan

# =========================
# CONFIG
# =========================
st.set_page_config(layout="wide")
st.title("🧠 MetastableX — SUS Digital Twin")

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

# =========================
# LOAD DATA (ROBUSTO)
# =========================
@st.cache_data
def load_data():
    df = pd.read_csv("data/timeseries_to.csv")
    cols = df.columns.tolist()

    if "municipio" in cols:
        return df

    if "MUNIC_RES" in cols:
        df["cod_mun_ibge_6"] = df["MUNIC_RES"].astype(str).str.zfill(6)
        return df

    if "cod_municipio" in cols:
        df["cod_mun_ibge_6"] = df["cod_municipio"].astype(str)
        return df

    raise Exception(f"Estrutura desconhecida: {cols}")

@st.cache_data
def load_municipios():
    df_mun = pd.read_csv("populacao_estimada_completa_spline.csv", sep=";")
    df_mun["cod_mun_ibge_6"] = df_mun["cod_mun_ibge_6"].astype(str)
    return df_mun[["cod_mun_ibge_6", "municipio"]].drop_duplicates()

df = load_data()

if "municipio" not in df.columns:
    df_mun = load_municipios()
    df = df.merge(df_mun, on="cod_mun_ibge_6", how="left")

df = df[df["municipio"].notna()]

# =========================
# EXPLICAÇÃO GLOBAL
# =========================
with st.expander("📘 Como interpretar este dashboard"):
    st.markdown("""
### 🧠 Este sistema analisa a dinâmica estrutural das internações hospitalares.

Não olhamos apenas valores absolutos, mas **como o sistema evolui no tempo**.

**Entropy (H)** → complexidade
**Coherence (I)** → estabilidade
**Energy (Φ)** → pressão estrutural

Regimes:
- RIGID → previsível, pouco adaptável
- METASTABLE → zona crítica adaptativa
- CHAOTIC → instável, possível colapso

O objetivo é detectar sinais precoces de instabilidade sistêmica.
""")

# =========================
# PREPROCESSAMENTO
# =========================
def preprocess(series):
    series = np.array(series, dtype=np.float32)
    series = series[~np.isnan(series)]
    if len(series) < 10:
        return None
    return (series - series.mean()) / (series.std() + 1e-6)

# =========================
# EXPLICAÇÃO MUNICÍPIO
# =========================
def explain_municipio(nome, series, history, mode="medical"):
    import numpy as np

    mid = len(series)//2

    var = np.var(series[mid:]) - np.var(series[:mid])

    def ac(x):
        return np.corrcoef(x[:-1], x[1:])[0,1] if len(x)>2 else 0

    ac_trend = ac(series[mid:]) - ac(series[:mid])

    H = history[-1]["H"]

    if mode == "medical":
        if var>0.1 and ac_trend>0.05:
            return f"{nome}: Sistema apresenta perda de resiliência progressiva."
        elif var>0.1:
            return f"{nome}: Sistema com aumento de instabilidade."
        elif H<0.5:
            return f"{nome}: Sistema rígido com baixa adaptabilidade."
        else:
            return f"{nome}: Sistema em equilíbrio dinâmico."

    else:
        return f"{nome} exhibits structural changes consistent with critical transition signals."

# =========================
# EXPLICAÇÃO ESTADO
# =========================
def explain_estado(df, mode="medical"):
    import numpy as np

    vars, acs = [], []

    for mun in df["municipio"].unique():
        s = df[df["municipio"]==mun]["taxa"].values
        s = preprocess(s)
        if s is None:
            continue

        mid = len(s)//2

        vars.append(np.var(s[mid:]) - np.var(s[:mid]))

        def ac(x):
            return np.corrcoef(x[:-1], x[1:])[0,1] if len(x)>2 else 0

        acs.append(ac(s[mid:]) - ac(s[:mid]))

    if len(vars)==0:
        return "Dados insuficientes."

    if mode=="medical":
        if np.mean(vars)>0.05 and np.mean(acs)>0.02:
            return "Estado apresenta perda de resiliência sistêmica."
        return "Estado relativamente estável."

    return "System shows early warning signals of instability."

# =========================
# SIDEBAR
# =========================
municipios = sorted(df["municipio"].unique())

selected = st.sidebar.selectbox("Município", municipios)

mode = st.sidebar.radio("Modo", ["Médico", "Científico"])

steps = st.sidebar.slider("Steps", 10, 200, 100)
k = st.sidebar.slider("k", 0.0, 1.0, 0.5)
sigma = st.sidebar.slider("σ", 0.0, 0.1, 0.01)

mode_internal = "medical" if mode=="Médico" else "paper"

# =========================
# SÉRIE
# =========================
st.subheader("📈 Série Temporal")

sub = df[df["municipio"]==selected]
series_raw = sub["taxa"].values
series = preprocess(series_raw)

st.line_chart(series_raw)

# =========================
# MODELO
# =========================
res = run_qwan(series)

regime = res["regime"]
risk = res["risk"]
history = res["history"]

col1, col2 = st.columns(2)

col1.metric("Regime", regime)
col2.metric("Risco", f"{risk:.4f}")

# =========================
# INTERPRETAÇÃO MUNICÍPIO
# =========================
st.subheader("🧠 Interpretação do Município")

st.info(explain_municipio(selected, series, history, mode_internal))

# =========================
# DINÂMICA
# =========================
st.markdown("""
### 📈 Evolução estrutural

Entropy → complexidade
Coherence → estabilidade
Energy → pressão
""")

H = [h["H"] for h in history]
I = [h["I"] for h in history]
Phi = [h["Phi"] for h in history]

st.line_chart(pd.DataFrame({
    "Entropy": H,
    "Coherence": I,
    "Energy": Phi
}))

# =========================
# RANKING
# =========================
st.subheader("🏆 Ranking")

ranking = []

for mun in municipios:
    s = df[df["municipio"]==mun]["taxa"].values
    s = preprocess(s)
    if s is None:
        continue

    try:
        r = run_qwan(s)
        ranking.append({
            "municipio": mun,
            "risco": r["risk"],
            "regime": r["regime"]
        })
    except:
        pass

ranking_df = pd.DataFrame(ranking).sort_values("risco", ascending=False)

st.dataframe(ranking_df.head(20))

# =========================
# EXPLICAÇÃO ESTADO
# =========================
st.subheader("🌍 Diagnóstico Estadual")

st.info(explain_estado(df, mode_internal))

# =========================
# ATLAS 2D
# =========================
st.subheader("🌍 Atlas")

H_vals = ranking_df["risco"]
I_vals = 1/(H_vals+1e-6)

fig, ax = plt.subplots()
ax.scatter(H_vals, I_vals)
st.pyplot(fig)

# =========================
# 3D
# =========================
st.subheader("🌐 Atlas 3D")

C,S,E=[],[],[]

for mun in municipios[:30]:
    s = df[df["municipio"]==mun]["taxa"].values
    s = preprocess(s)
    if s is None:
        continue

    try:
        r = run_qwan(s)
        last = r["history"][-1]
        C.append(last["H"])
        S.append(last["I"])
        E.append(last["Phi"])
    except:
        pass

fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
ax.scatter(C,S,E)
st.pyplot(fig)

# =========================
# SIMULAÇÃO
# =========================
st.subheader("🧪 Simulação")

if st.button("Simular"):
    from metastablex.qwan.dynamics import evolve

    x = torch.tensor(series, dtype=torch.float32, device=device, requires_grad=True)
    _, hist = evolve(x, steps=steps, k=k, sigma=sigma)

    st.line_chart([h["H"] for h in hist])
