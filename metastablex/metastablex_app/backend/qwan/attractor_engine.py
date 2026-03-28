import numpy as np

class AttractorDetector:

    def __init__(self):
        self.history = []

    def update(self, field):

        flat = field.flatten()
        self.history.append(flat)

        if len(self.history) > 50:
            self.history.pop(0)

    def detect(self):

        if len(self.history) < 20:
            return "unknown"

        data = np.array(self.history)

        # variância total
        var = np.var(data)

        # repetição (ciclo)
        diffs = np.linalg.norm(data[1:] - data[:-1], axis=1)
        periodic = np.std(diffs) < 0.01

        if var < 0.001:
            return "fixed_point"

        if periodic:
            return "limit_cycle"

        return "strange_attractor"
