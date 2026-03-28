import torch
from .energy import entropy, coherence, energy_free

def compute_gradients(x, alpha=1.0, beta=1.0):

    x = x.clone().detach().requires_grad_(True)

    E = energy_free(x)
    H = entropy(x)
    I = coherence(x)

    grad_E = torch.autograd.grad(E, x, retain_graph=True, create_graph=True)[0]
    grad_H = torch.autograd.grad(H, x, retain_graph=True, create_graph=True)[0]

    # 🔥 CORREÇÃO CRÍTICA
    if I.requires_grad:
        grad_I = torch.autograd.grad(I, x, create_graph=True)[0]
    else:
        grad_I = torch.zeros_like(x)

    return grad_E, grad_H, grad_I
