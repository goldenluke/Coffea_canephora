def contexto_fisica_matematica():
    return r"""
=== FÍSICA ESTATÍSTICA APLICADA ===

1. Energia Livre (aproximação empírica):

F(x) = -log(P(x))

onde:
- P(x): densidade estimada da variável (ex: taxa epidemiológica)
- F(x): energia livre → menor valor = estado mais estável

Interpretação:
- mínimos locais → estados metaestáveis
- mudanças abruptas → transições de fase

---

2. Entropia Temporal:

H = - Σ p(x) log p(x)

onde:
- p(x): distribuição das observações em uma janela temporal

Interpretação:
- alta entropia → sistema desorganizado
- baixa entropia → regime estável

---

3. Critical Slowing Down:

AC(1) = Corr(x_t, x_{t-1})

Variância:
Var(x) ↑ antes de transições críticas

Interpretação:
- aumento de autocorrelação → perda de resiliência
- aumento da variância → instabilidade crescente

---

4. Sistema Dinâmico:

dx/dt = f(x, θ)

onde:
- x: estado epidemiológico
- θ: parâmetros do sistema

Estados estacionários:
f(x*) = 0

---

"""


def contexto_epidemiologia_matematica():
    return r"""
=== EPIDEMIOLOGIA MATEMÁTICA ===

1. Taxa por 100k habitantes:

Taxa = (Casos / População) * 100000

---

2. Crescimento relativo:

r_t = (x_t - x_{t-1}) / x_{t-1}

Interpretação:
- r_t > 0.5 → crescimento explosivo (surto)

---

3. Modelo SIR:

dS/dt = -β S I
dI/dt = β S I - γ I
dR/dt = γ I

onde:
- S: suscetíveis
- I: infectados
- R: recuperados
- β: taxa de transmissão
- γ: taxa de recuperação

Número básico de reprodução:

R0 = β / γ

Interpretação:
- R0 > 1 → epidemia cresce
- R0 < 1 → epidemia decai

---

4. Série temporal:

x_t = número de casos no tempo t

Análise:
- tendência → regressão linear
- volatilidade → desvio padrão

---

"""


def contexto_hmm_matematico():
    return r"""
=== HIDDEN MARKOV MODEL (HMM) ===

Estados ocultos:
Z_t ∈ {1, 2, ..., K}

Observações:
X_t ~ P(X | Z_t)

Probabilidade de transição:

P(Z_t = j | Z_{t-1} = i) = A_ij

Probabilidade de emissão:

P(X_t | Z_t = k) ~ N(μ_k, σ_k)

Objetivo:
inferir sequência de estados ocultos:

argmax P(Z | X)

Interpretação:
- cada estado = regime epidemiológico
- mudanças de estado = transições de fase

---

"""


def contexto_clustering_matematico():
    return r"""
=== CLUSTERIZAÇÃO (K-MEANS) ===

Objetivo:

min Σ ||x_i - μ_k||²

onde:
- μ_k: centro do cluster

Interpretação:
- cada cluster → perfil epidemiológico
- agrupamento temporal → regimes dinâmicos

---

"""


def contexto_completo():
    return f"""
{contexto_fisica_matematica()}

{contexto_epidemiologia_matematica()}

{contexto_hmm_matematico()}

{contexto_clustering_matematico()}

=== INTERPRETAÇÃO GLOBAL ===

O sistema modela epidemiologia como um sistema fora do equilíbrio:

- Estados metaestáveis → padrões persistentes
- Transições de fase → surtos epidemiológicos
- Energia livre → estabilidade do sistema
- Entropia → desorganização
- HMM → identificação de regimes ocultos
- SIR → dinâmica mecanicista da doença

Objetivo final:
detectar mudanças estruturais no sistema antes que eventos críticos ocorram.
"""
