def interpretar_tendencia(serie):
    if serie.iloc[-1] > serie.iloc[0]:
        return "Crescente"
    elif serie.iloc[-1] < serie.iloc[0]:
        return "Decrescente"
    return "Estável"

def interpretar_volatilidade(serie):
    cv = serie.std() / serie.mean()
    if cv > 0.5:
        return "Alta instabilidade"
    elif cv > 0.2:
        return "Moderada"
    return "Baixa"

def interpretar_valor(valor, media, desvio):
    if valor > media + 2*desvio:
        return "Outlier alto"
    elif valor < media - 2*desvio:
        return "Outlier baixo"
    return "Normal"
