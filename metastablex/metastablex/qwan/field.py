import torch

class QWANField:
    def __init__(self, series):
        if not isinstance(series, torch.Tensor):
            series = torch.tensor(series, dtype=torch.float32)

        self.x = series.clone().detach().requires_grad_(True)
