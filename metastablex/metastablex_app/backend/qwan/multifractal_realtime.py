from collections import deque
from .multifractal import mfdfa

class OnlineMultifractal:

    def __init__(self, window=300):
        self.buffer = deque(maxlen=window)

    def update(self, value):
        self.buffer.append(value)

    def compute(self):
        if len(self.buffer) < 100:
            return None

        alpha, f_alpha = mfdfa(list(self.buffer))
        return {
            "alpha": alpha.tolist(),
            "f": f_alpha.tolist()
        }
