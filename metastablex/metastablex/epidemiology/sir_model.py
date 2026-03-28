import numpy as np
from scipy.integrate import odeint

def sir(y, t, beta, gamma):
    S, I, R = y

    dSdt = -beta * S * I
    dIdt = beta * S * I - gamma * I
    dRdt = gamma * I

    return dSdt, dIdt, dRdt


def rodar_sir(populacao, infectados_iniciais, dias=100):

    S0 = populacao - infectados_iniciais
    I0 = infectados_iniciais
    R0 = 0

    y0 = S0, I0, R0

    t = np.linspace(0, dias, dias)

    beta = 0.3
    gamma = 0.1

    ret = odeint(sir, y0, t, args=(beta, gamma))
    S, I, R = ret.T

    return t, S, I, R
