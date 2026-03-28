import torch.nn.functional as F

def coarse_grain(x, factor=2):
    # downsample temporal
    return F.avg_pool1d(x, kernel_size=factor, stride=factor)

def rg_flow(x, levels=4):
    scales = []

    current = x

    for i in range(levels):
        current = coarse_grain(current, factor=2)
        scales.append(current)

    return scales

def build_atlas3d(history, municipios):
    atlas = []

    last = history[-1]

    for i, mun in enumerate(municipios):
        C = last["H"][i].item()
        S = last["I"][i].item()
        E = last["G"][i].item()

        atlas.append({
            "municipio": mun,
            "C": C,
            "S": S,
            "E": E
        })

    return atlas
