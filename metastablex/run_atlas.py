from metastablex.qwan.data_batch import build_batch
from metastablex.qwan.batch_engine import evolve_batch
from metastablex.atlas.regime_atlas import build_atlas
from metastablex.plots.paper import *

batch, municipios = build_batch(df)
batch = batch.to("cuda").requires_grad_()

x_final, history = evolve_batch(batch)

atlas = build_atlas(history, municipios)

plot_phase_diagram(atlas)
plot_risk(atlas)
plot_dynamics(history)
