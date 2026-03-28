import numpy as np
import pandas as pd

from metastablex.detectors.universal_detector import UniversalComplexityDetector


class UniversalComplexityScanner:

    def __init__(self):

        self.detector = UniversalComplexityDetector()

    def scan_series(self, ts):

        result = self.detector.analyze(ts)

        features = result["features"]

        vector = [

            features["variance"],
            features["ac1"],
            features["entropy"],
            features["fisher"],
            features["dfa"],
            features["volatility"]

        ]

        return {

            "vector": vector,
            "regime": result["regime"],
            "universality": result["universality_class"],
            "risk": result["tipping_risk"]

        }

    def scan_dataset(self, dataset):

        results = []

        for name, ts in dataset.items():

            r = self.scan_series(ts)

            r["name"] = name

            results.append(r)

        return results
