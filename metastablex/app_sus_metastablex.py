import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pysus.online_data.SIH import SIH

# ==========================================================
# CONFIGURAÇÃO
# ==========================================================

st.set_page_config(
    page_title="SUS MetastableX",
    layout="wide"
)

st.title("🇧🇷 Monitor Estrutural do SUS — MetastableX")

st.write("""
Dashboard experimental para análise de **dinâmica de sistemas complexos no SUS**.

O sistema utiliza:

• dados reais do **SIH/DATASUS**
• métricas de **física estatística**
• detecção de **instabilidade sistêmica**

Objetivo: identificar **sinais precoces de transições críticas no sistema de saúde**.
""")

# ==========================================================
# SIDEBAR
# ==========================================================

st.sidebar.header("Parâmetros")

uf = st.sidebar.selectbox(
    "Estado",
    ["SP","RJ","MG","BA","TO","PR","RS"]
)

ano = st.sidebar.slider(
    "Ano",
    2015,
    2024,
    2023
)

cid = st.sidebar.text_input(
    "Prefixo CID-10",
    "J"
)

janela = st.sidebar.slider(
    "Janela móvel",
    7,
    30,
    14
)

# ==========================================================
# DOWNLOAD DE DADOS
# ==========================================================

@st.cache_data
def carregar_sih(uf, ano):

    sih = SIH().load()

    arquivos = sih.get_files(
        group="RD",
        uf=uf,
        year=ano
    )

    if not arquivos:
        return pd.DataFrame()

    df = sih.download(arquivos[0]).to_dataframe()

    return df

with st.spinner("Baixando dados do DATASUS..."):

    df = carregar_sih(uf,ano)

if df.empty:

    st.warning("Não foi possível carregar os dados.")
    st.stop()

# ==========================================================
# FILTRO CID
# ==========================================================

df = df[df["DIAG_PRINC"].astype(str).str.startswith(cid)]

df["DT_INTER"] = pd.to_datetime(df["DT_INTER"],errors="coerce")

serie = df.groupby("DT_INTER").size().sort_index()

# ==========================================================
# MOTOR DE COMPLEXIDADE
# ==========================================================

class MotorComplexidade:

    def __init__(self,ts):

        self.ts = np.array(ts)

    def autocorrelacao(self):

        return pd.Series(self.ts).autocorr(lag=1)

    def variancia(self):

        return np.var(self.ts)

    def entropia(self):

        hist,_ = np.histogram(self.ts,bins=20)

        p = hist / hist.sum()

        p = p[p>0]

        return -np.sum(p*np.log(p))

    def dfa(self):

        ts = self.ts

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
                         np.polyfit(
                             np.arange(n),
                             y[i*n:(i+1)*n],1),
                         np.arange(n)
                     )
                    )**2
                )
                for i in range(seg)
            ]))

            rms.append(val)

        if len(rms) < 2:
            return 0.5

        return np.polyfit(np.log(n_vals[:len(rms)]),np.log(rms),1)[0]

motor = MotorComplexidade(serie.values)

ac1 = motor.autocorrelacao()
var = motor.variancia()
ent = motor.entropia()
dfa = motor.dfa()

# ==========================================================
# DETECÇÃO DE REGIME
# ==========================================================

def detectar_regime(ts):

    ac1 = pd.Series(ts).autocorr(lag=1)

    if ac1 > 0.7:
        return "CRÍTICO"

    elif ac1 > 0.5:
        return "METAESTÁVEL"

    return "ESTÁVEL"

regime = detectar_regime(serie.values)

# ==========================================================
# MÉTRICAS
# ==========================================================

st.subheader("Indicadores do Sistema")

c1,c2,c3,c4,c5 = st.columns(5)

c1.metric("Autocorrelação",round(ac1,3))
c2.metric("Variância",round(var,3))
c3.metric("Entropia",round(ent,3))
c4.metric("Expoente DFA",round(dfa,3))
c5.metric("Regime",regime)

# ==========================================================
# SÉRIE TEMPORAL
# ==========================================================

st.subheader("Série Temporal de Internações")

fig,ax = plt.subplots(figsize=(12,4))

ax.plot(serie.index,serie.values)

ax.set_title("Internações hospitalares")

st.pyplot(fig)

# ==========================================================
# INDICADORES DE ALERTA PRECOCE
# ==========================================================

st.subheader("Indicadores de Alerta Precoce")

var_movel = serie.rolling(janela).var()

ac1_movel = serie.rolling(janela).apply(
    lambda x: pd.Series(x).autocorr(lag=1)
)

fig2,ax2 = plt.subplots(2,1,figsize=(12,6))

ax2[0].plot(var_movel)
ax2[0].set_title("Variância móvel")

ax2[1].plot(ac1_movel)
ax2[1].set_title("Autocorrelação móvel")

plt.tight_layout()

st.pyplot(fig2)

# ==========================================================
# INTERPRETAÇÃO
# ==========================================================

st.subheader("Interpretação das Métricas")

interpretacao = f"""
### Autocorrelação (AC1)

Valor observado: **{ac1:.3f}**

- mede quanto o sistema depende do estado anterior
- valores altos indicam **critical slowing down**

---

### Variância

Valor observado: **{var:.3f}**

- aumento da variância indica **instabilidade crescente**

---

### Entropia

Valor observado: **{ent:.3f}**

- mede a **complexidade da série temporal**

interpretação aproximada:

• baixa entropia → sistema rígido
• entropia moderada → sistema adaptativo
• entropia muito alta → comportamento caótico

---

### Expoente DFA

Valor observado: **{dfa:.3f}**

interpretação:

• DFA ≈ 0.5 → ruído aleatório
• DFA 0.6–0.8 → memória de longo alcance
• DFA > 0.9 → comportamento altamente persistente

---

### Regime do sistema

Classificação atual: **{regime}**
"""

st.markdown(interpretacao)

# ==========================================================
# DIAGNÓSTICO FINAL
# ==========================================================

st.subheader("Diagnóstico Sistêmico")

if regime == "CRÍTICO":

    st.error("""
O sistema apresenta sinais de **transição crítica**.

Possíveis interpretações:

• crescimento acelerado de internações
• aproximação de pico epidêmico
• pressão sobre capacidade hospitalar
""")

elif regime == "METAESTÁVEL":

    st.warning("""
O sistema encontra-se em **regime metaestável**.

Isso significa que pequenas perturbações podem gerar mudanças abruptas.
""")

else:

    st.success("""
O sistema aparenta estar em **regime estável**.
""")
