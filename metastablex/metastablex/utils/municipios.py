import pandas as pd

def carregar_populacao(arquivo):
    df = pd.read_csv(arquivo, sep=";")
    df.columns = df.columns.str.lower()

    df["uf"] = df["uf"].str.upper()
    df["municipio"] = df["municipio"].str.upper()

    return df


def filtrar_populacao(arquivo_populacao, uf=None, ano=None):
    df = carregar_populacao(arquivo_populacao)

    if uf:
        df = df[df["uf"] == uf]

    if ano:
        df = df[df["ano"] == ano]

    return df

def codigo_para_nome(cod_ibge):
    """
    MOCK simples — substitua depois por base real
    """
    return str(cod_ibge)
