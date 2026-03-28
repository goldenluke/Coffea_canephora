import numpy as np
from metastablex.physics.engine import MetastableXEngine

def generate_atlas(
    potential_factory,
    param_range,
    noise_range,
    steps=1000,
    samples=20
):

    atlas_data = []

    for p in param_range:

        for noise in noise_range:

            for _ in range(samples):

                potential = potential_factory(p)

                engine = MetastableXEngine(
                    potential=potential,
                    noise=noise,
                    steps=steps
                )

                series = engine.simulate()

                atlas_data.append({
                    "param": p,
                    "noise": noise,
                    "series": series
                })

    return atlas_data
