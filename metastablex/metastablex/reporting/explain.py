def explain_municipio_advanced(nome, series, history, mode="medical"):
    import numpy as np

    if len(series) < 10:
        return "Insufficient time series for structural analysis."

    # =========================
    # MÉTRICAS
    # =========================
    mid = len(series) // 2

    var_start = np.var(series[:mid])
    var_end = np.var(series[mid:])
    var_trend = var_end - var_start

    def autocorr(x):
        if len(x) < 2:
            return 0
        return np.corrcoef(x[:-1], x[1:])[0,1]

    ac_start = autocorr(series[:mid])
    ac_end = autocorr(series[mid:])
    ac_trend = ac_end - ac_start

    H = history[-1].get("H", 0)
    I = history[-1].get("I", 0)

    # =========================
    # CLASSIFICAÇÕES
    # =========================
    instability = var_trend > 0.1
    memory = ac_trend > 0.05
    chaotic = H > 1.5
    rigid = H < 0.5

    # =========================
    # 🏥 MODO MÉDICO
    # =========================
    if mode == "medical":

        texto = f"{nome}: "

        if instability and memory:
            texto += "Sistema apresenta padrão compatível com perda de resiliência progressiva, caracterizado por aumento simultâneo da variabilidade e da memória temporal."

        elif instability:
            texto += "Sistema com aumento de variabilidade, sugerindo instabilidade estrutural crescente."

        elif rigid:
            texto += "Sistema com comportamento rígido, baixa variabilidade e possível limitação adaptativa."

        elif chaotic:
            texto += "Sistema com dinâmica altamente complexa e possivelmente desorganizada."

        else:
            texto += "Sistema em equilíbrio dinâmico, sem sinais evidentes de instabilidade estrutural."

        # complemento clínico
        if memory:
            texto += " Observa-se aumento de autocorrelação, consistente com desaceleração crítica."

        return texto

    # =========================
    # 🧠 MODO PAPER (NATURE)
    # =========================
    elif mode == "paper":

        texto = f"{nome} exhibits "

        componentes = []

        if instability:
            componentes.append("an increase in variance")
        if memory:
            componentes.append("elevated lag-1 autocorrelation")
        if chaotic:
            componentes.append("high entropy levels")
        if rigid:
            componentes.append("low entropy regime")

        if not componentes:
            return f"{nome} remains within a stable dynamical regime with no significant structural shifts."

        texto += ", ".join(componentes)

        texto += ", indicating "

        if instability and memory:
            texto += "a loss of resilience consistent with critical slowing down."

        elif instability:
            texto += "emerging instability in the system dynamics."

        elif chaotic:
            texto += "a transition toward a high-complexity regime."

        elif rigid:
            texto += "a strongly constrained dynamical regime."

        else:
            texto += "a structurally stable regime."

        texto += " These patterns are consistent with early-warning signals of critical transitions in complex systems."

        return texto

    return "Invalid mode"

def explain_estado(df, mode="medical"):
    import numpy as np

    municipios = df["municipio"].unique()

    variancias = []
    autocorrs = []
    entropias = []

    def autocorr(x):
        if len(x) < 2:
            return 0
        return np.corrcoef(x[:-1], x[1:])[0,1]

    for mun in municipios:
        sub = df[df["municipio"] == mun]

        if "taxa" not in sub.columns:
            continue

        s = sub["taxa"].values.astype(float)
        s = s[~np.isnan(s)]

        if len(s) < 10:
            continue

        mid = len(s)//2

        variancias.append(np.var(s[mid:]) - np.var(s[:mid]))
        autocorrs.append(autocorr(s[mid:]) - autocorr(s[:mid]))
        entropias.append(np.std(s))

    if len(variancias) == 0:
        return "Dados insuficientes."

    var_mean = np.mean(variancias)
    ac_mean = np.mean(autocorrs)
    heterogeneity = np.std(variancias)

    instability = var_mean > 0.05
    memory = ac_mean > 0.02
    hetero = heterogeneity > 0.1

    if mode == "medical":
        texto = "O sistema estadual apresenta "

        if instability and memory:
            texto += "perda de resiliência sistêmica."
        elif instability:
            texto += "instabilidade crescente."
        else:
            texto += "comportamento estável."

        if hetero:
            texto += " Há heterogeneidade relevante entre municípios."

        return texto

    else:
        texto = "The system exhibits "

        comps = []
        if instability:
            comps.append("increasing variance")
        if memory:
            comps.append("rising autocorrelation")
        if hetero:
            comps.append("high heterogeneity")

        if not comps:
            return "System remains stable."

        texto += ", ".join(comps)
        texto += ", suggesting systemic instability."

        return texto
