import numpy as np
from metastablex.physics.engine import MetastableXEngine
from metastablex.atlas3d.metrics import compute_3d_metrics

def build_atlas3d(potential_factory,param_range,noise_range):

    points = []

    for p in param_range:

        for noise in noise_range:

            potential = potential_factory(p)

            engine = MetastableXEngine(
                potential=potential,
                noise=noise,
                steps=1500
            )

            series = engine.simulate()

            c,s,e = compute_3d_metrics(series)

            points.append((c,s,e))

    return np.array(points)
