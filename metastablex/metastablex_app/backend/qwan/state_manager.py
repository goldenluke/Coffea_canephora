import numpy as np

class StateManager:
    def __init__(self):
        self.snapshots = []
        self.max_snapshots = 200

    def add(self, H, I, Phi):
        self.snapshots.append([H, I, Phi])
        if len(self.snapshots) > self.max_snapshots:
            self.snapshots.pop(0)

    def get_array(self):
        return np.array(self.snapshots) if self.snapshots else np.zeros((1,3))

state_manager = StateManager()
