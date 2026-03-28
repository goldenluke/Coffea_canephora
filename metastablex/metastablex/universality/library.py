import numpy as np

class UniversalityLibrary:

    def __init__(self):

        self.classes = {

            "ordered": {
                "dfa": (0.0, 0.4),
                "entropy": (0.0, 1.0),
                "ac1": (0.5, 1.0)
            },

            "chaotic": {
                "dfa": (0.5, 1.5),
                "entropy": (1.5, 5.0),
                "ac1": (-0.3, 0.3)
            },

            "critical_qwan": {
                "dfa": (0.6, 1.0),
                "entropy": (1.0, 2.5),
                "ac1": (0.2, 0.6)
            },

            "percolation": {
                "variance": (0.5, 10),
                "ac1": (0.3, 0.9)
            },

            "glassy": {
                "dfa": (0.9, 1.5),
                "entropy": (0.5, 2),
                "ac1": (0.7, 1)
            }

        }

    def classify(self, metrics):

        scores = {}

        for name, conditions in self.classes.items():

            score = 0

            for k,(low,high) in conditions.items():

                if k in metrics and low <= metrics[k] <= high:
                    score += 1

            scores[name] = score

        return max(scores, key=scores.get)
