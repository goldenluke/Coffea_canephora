import numpy as np

# Ginzburg-Landau (bifurcação)
def ginzburg_landau(a=0.1,b=1):

    def U(x):
        return -a*x**2 + b*x**4

    return U

# potencial logístico (epidemiologia)
def epidemic_potential(beta=1):

    def U(x):
        return -beta*x + x**2

    return U

# mercado financeiro
def market_potential(vol=1):

    def U(x):
        return vol*(x**2) + 0.1*(x**3)

    return U

# fisiologia (homeostase)
def physiological_potential(x0=0):

    def U(x):
        return (x-x0)**2

    return U
