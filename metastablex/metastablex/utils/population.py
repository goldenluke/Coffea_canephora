import pandas as pd


def filtrar_populacao(arquivo, uf, ano):

    df = pd.read_csv(arquivo, sep=";")

    df = df[(df["UF"] == uf) & (df["ano"] == ano)]

    return df
