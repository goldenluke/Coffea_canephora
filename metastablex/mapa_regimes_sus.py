import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pysus.online_data.SIH import SIH
from scipy import stats

# ==========================================================
# CONFIG
# ==========================================================

st.set_page_config(layout="wide")

st.title("🧠 Laboratório Analítico do SUS — Municípios")

ano = st.slider("Ano",2018,2024,2023)

# ==========================================================
# POPULAÇÃO
# ==========================================================

@st.cache_data
def carregar_pop():

    pop = pd.read_csv(
        "populacao_estimada_completa_spline.csv",
        sep=";"
    )

    pop["cod_mun_ibge_6"] = pop["cod_mun_ibge_6"].astype(str)

    pop_to = pop[pop["UF"] == "TO"]

    return pop_to

pop = carregar_pop()

# ==========================================================
# SIH
# ==========================================================

@st.cache_data
def carregar_sih():

    sih = SIH().load()

    files = sih.get_files(
        group="RD",
        uf="TO",
        year=ano
    )

    if not files:
        return None

    df = sih.download(files[0]).to_dataframe()

    df["DT_INTER"] = pd.to_datetime(df["DT_INTER"],errors="coerce")

    return df

df = carregar_sih()

if df is None:
    st.stop()

# ==========================================================
# MUNICÍPIO
# ==========================================================

df["MUNICIPIO_IBGE"] = df["MUNIC_RES"].astype(str).str[:6]

df = df.merge(
    pop,
    left_on="MUNICIPIO_IBGE",
    right_on="cod_mun_ibge_6",
    how="left"
)

df["municipio"] = df["municipio"]

municipios = sorted(df["municipio"].dropna().unique())

municipio = st.selectbox(
    "Selecionar município",
    municipios
)

sub = df[df["municipio"] == municipio]

ts = sub.groupby("DT_INTER").size()

# ==========================================================
# MÉTRICAS
# ==========================================================

mean = np.mean(ts)

median = np.median(ts)

var = np.var(ts)

std = np.std(ts)

cv = std / mean if mean > 0 else 0

skew = stats.skew(ts)

kurt = stats.kurtosis(ts)

ac1 = pd.Series(ts).autocorr(lag=1)

trend = np.polyfit(range(len(ts)),ts,1)[0]

vol = std

# ==========================================================
# ENTROPIA
# ==========================================================

hist,_ = np.histogram(ts,bins=20)

p = hist/hist.sum()

p = p[p>0]

entropy = -np.sum(p*np.log(p))

# ==========================================================
# DFA
# ==========================================================

def dfa(ts):

    ts = np.array(ts)

    y = np.cumsum(ts - np.mean(ts))

    n_vals = np.unique(np.logspace(1,2,8).astype(int))

    rms = []

    for n in n_vals:

        seg = len(y)//n

        if seg == 0:
            continue

        val = np.sqrt(np.mean([
            np.mean(
                (y[i*n:(i+1)*n] -
                 np.polyval(
                     np.polyfit(np.arange(n),y[i*n:(i+1)*n],1),
                     np.arange(n)
                 ))**2
            )
            for i in range(seg)
        ]))

        rms.append(val)

    if len(rms) < 2:
        return 0.5

    return np.polyfit(np.log(n_vals[:len(rms)]),np.log(rms),1)[0]

dfa_val = dfa(ts)

# ==========================================================
# PAINEL DE MÉTRICAS
# ==========================================================

st.subheader("📊 Métricas")

cols = st.columns(6)

cols[0].metric("Média",round(mean,2))
cols[1].metric("Mediana",round(median,2))
cols[2].metric("Variância",round(var,2))
cols[3].metric("AC1",round(ac1,3))
cols[4].metric("Entropia",round(entropy,3))
cols[5].metric("DFA",round(dfa_val,3))

# ==========================================================
# SÉRIE TEMPORAL
# ==========================================================

st.subheader("📈 Série temporal")

fig,ax = plt.subplots(figsize=(10,4))

ax.plot(ts.index,ts.values)

st.pyplot(fig)

# ==========================================================
# EARLY WARNING
# ==========================================================

window = 14

var_roll = ts.rolling(window).var()

ac_roll = ts.rolling(window).apply(
    lambda x: pd.Series(x).autocorr(lag=1)
)

fig2,ax2 = plt.subplots(2,1,figsize=(10,6))

ax2[0].plot(var_roll)

ax2[0].set_title("Variância móvel")

ax2[1].plot(ac_roll)

ax2[1].set_title("Autocorrelação móvel")

plt.tight_layout()

st.pyplot(fig2)

# ==========================================================
# RELATÓRIO AUTOMÁTICO
# ==========================================================

st.subheader("🧠 Análise automática")

analysis = f"""

### Estatísticas

Média: {mean:.2f}

Variância: {var:.2f}

Coeficiente de variação: {cv:.2f}

---

### Estrutura da distribuição

Skewness: {skew:.2f}

Kurtosis: {kurt:.2f}

---

### Dinâmica temporal

Autocorrelação (AC1): {ac1:.2f}

Tendência: {trend:.2f}

Volatilidade: {vol:.2f}

---

### Complexidade

Entropia: {entropy:.2f}

DFA: {dfa_val:.2f}

"""

st.markdown(analysis)

# ==========================================================
# INTERPRETAÇÃO
# ==========================================================

st.subheader("⚕️ Interpretação")

if ac1 > 0.7:

    st.error("""
Sistema em regime crítico.

Indícios de instabilidade hospitalar.
""")

elif ac1 > 0.5:

    st.warning("""
Sistema em regime metastável.

Mudanças estruturais podem ocorrer.
""")

else:

    st.success("""
Sistema aparentemente estável.
""")
