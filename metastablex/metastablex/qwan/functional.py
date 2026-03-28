import torch
import torch.nn.functional as F

def local_mean(x, kernel_size=5):
    kernel = torch.ones(1,1,kernel_size) / kernel_size
    x = x.view(1,1,-1)
    return F.conv1d(x, kernel, padding=kernel_size//2).view(-1)

def functional(x, alpha=1.0, beta=1.0, gamma=1.0, x0=0):
    mean = local_mean(x)

    G = 0.5 * (x - x0)**2
    H = (x - mean)**2
    I = (torch.gradient(x)[0])**2

    Phi = gamma*G - alpha*H + beta*I

    return Phi.mean(), {
        "G": G.mean(),
        "H": H.mean(),
        "I": I.mean()
    }
