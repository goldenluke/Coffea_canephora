import numpy as np
from metastablex.tensor.multiscale import multiscale_series
from metastablex.tensor.metrics import compute_scale_metrics

def build_regime_tensor(ts, scales):

    tensor = []

    series_scales = multiscale_series(ts,scales)

    for scale,series in zip(scales,series_scales):

        c,s,e = compute_scale_metrics(series)

        tensor.append([c,s,e,scale])

    return np.array(tensor)
