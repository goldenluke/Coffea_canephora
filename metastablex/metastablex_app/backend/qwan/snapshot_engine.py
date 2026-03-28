import torch

class SnapshotEngine:

    def __init__(self, max_snapshots=200):
        self.snapshots = []
        self.max_snapshots = max_snapshots

    def save(self, field, meta):

        snap = {
            "field": field.detach().cpu().tolist(),
            "meta": meta
        }

        self.snapshots.append(snap)

        if len(self.snapshots) > self.max_snapshots:
            self.snapshots.pop(0)

    def get(self, idx):
        if 0 <= idx < len(self.snapshots):
            return self.snapshots[idx]
        return None

    def all(self):
        return self.snapshots
