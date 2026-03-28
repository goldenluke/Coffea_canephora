import numpy as np
import pandas as pd
from scipy import stats

# =====================================
# COMPLEXITY METRICS
# =====================================

def autocorr_lag1(ts):

    ts = np.array(ts)

    if len(ts) < 3:
        return 0

    return np.corrcoef(ts[:-1], ts[1:])[0,1]


def shannon_entropy(ts):

    hist,_ = np.histogram(ts,bins=30,density=True)

    p = hist + 1e-12

    return -np.sum(p*np.log(p))


def fisher_information(ts):

    hist,_ = np.histogram(ts,bins=30,density=True)

    p = hist + 1e-12

    return 4*np.sum(np.diff(np.sqrt(p))**2)


def volatility(ts):

    return np.std(np.diff(ts))


# =====================================
# FRACTAL MEMORY (DFA)
# =====================================

def dfa_alpha(ts):

    ts = np.array(ts)

    y = np.cumsum(ts - np.mean(ts))

    n_vals = np.unique(np.logspace(1,2,8).astype(int))

    rms_vals = []

    for n in n_vals:

        segments = len(y)//n

        if segments == 0:
            continue

        rms = np.sqrt(np.mean([

            np.mean(

                (y[i*n:(i+1)*n] -

                 np.polyval(

                     np.polyfit(

                         np.arange(n),

                         y[i*n:(i+1)*n],1

                     ),

                     np.arange(n)

                 )

                )**2

            )

            for i in range(segments)

        ]))

        rms_vals.append(rms)

    if len(rms_vals) < 2:
        return 0.5

    return np.polyfit(

        np.log(n_vals[:len(rms_vals)]),

        np.log(rms_vals),1

    )[0]


# =====================================
# UNIVERSAL COMPLEXITY DETECTOR
# =====================================

class UniversalComplexityDetector:

    def __init__(self):

        pass


    def compute_features(self, ts):

        ts = np.array(ts)

        returns = np.diff(ts)

        features = {}

        features["variance"] = np.var(returns)

        features["ac1"] = autocorr_lag1(returns)

        features["entropy"] = shannon_entropy(returns)

        features["fisher"] = fisher_information(returns)

        features["dfa"] = dfa_alpha(returns)

        features["volatility"] = volatility(ts)

        return features


    # ---------------------------------
    # REGIME DETECTION
    # ---------------------------------

    def detect_regime(self, features):

        ac1 = features["ac1"]
        var = features["variance"]
        entropy = features["entropy"]

        if ac1 > 0.7 and entropy < 1.0:
            return "ORDERED"

        if ac1 < 0.2 and entropy > 2.0:
            return "CHAOTIC"

        if 0.3 < ac1 < 0.6:
            return "METASTABLE_QWAN"

        return "TRANSITIONAL"


    # ---------------------------------
    # UNIVERSALITY CLASS
    # ---------------------------------

    def classify_universality(self, features):

        dfa = features["dfa"]
        ac1 = features["ac1"]
        var = features["variance"]

        if dfa < 0.4:
            return "Ordered-like"

        if 0.6 < dfa < 1.0 and 0.2 < ac1 < 0.6:
            return "Critical (QWAN)"

        if var > 1 and ac1 > 0.4:
            return "Percolation-like"

        if dfa > 1.2:
            return "Glassy"

        return "Chaotic"


    # ---------------------------------
    # CRITICAL TRANSITION RISK
    # ---------------------------------

    def tipping_risk(self, features):

        ac1 = features["ac1"]
        var = features["variance"]
        fisher = features["fisher"]

        risk = (

            (ac1 + 1)/2 +

            var/(var+1) +

            1/(fisher+1)

        )/3

        return min(max(risk,0),1)


    # ---------------------------------
    # MAIN DETECTOR
    # ---------------------------------

    def analyze(self, ts):

        features = self.compute_features(ts)

        regime = self.detect_regime(features)

        universality = self.classify_universality(features)

        risk = self.tipping_risk(features)

        return {

            "features": features,

            "regime": regime,

            "universality_class": universality,

            "tipping_risk": risk

        }
