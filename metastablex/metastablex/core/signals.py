# metastablex/core/signals.py

import numpy as np
import pandas as pd
from scipy import stats

# ========================================
# SÉRIES TEMPORAIS SINTÉTICAS
# ========================================

def synthetic_series(n=100, freq=1.0, noise_level=0.1, seed=None):
    """
    Gera uma série temporal sintética para testes.

    Parâmetros:
    ----------
    n : int
        Número de pontos da série
    freq : float
        Frequência do sinal senoidal base
    noise_level : float
        Desvio padrão do ruído adicionado
    seed : int ou None
        Semente para reprodutibilidade

    Retorna:
    -------
    ts : np.ndarray
        Série temporal sintética
    """
    if seed is not None:
        np.random.seed(seed)
    t = np.linspace(0, 10, n)
    ts = np.sin(2 * np.pi * freq * t) + noise_level * np.random.randn(n)
    return ts

# ========================================
# SENSORES BÁSICOS DE COMPLEXIDADE
# ========================================

def rolling_volatility(ts, window=10):
    """
    Calcula volatilidade (desvio padrão móvel) de uma série.
    """
    ts = pd.Series(ts)
    return ts.rolling(window).std().to_numpy()

def autocorr_lag1(ts):
    """
    Calcula autocorrelação de lag 1
    """
    ts = pd.Series(ts)
    return ts.autocorr(lag=1)

def skewness(ts):
    """
    Calcula skewness (assimetria) da série
    """
    return stats.skew(ts)

def kurtosis(ts):
    """
    Calcula kurtosis (curtose) da série
    """
    return stats.kurtosis(ts)
