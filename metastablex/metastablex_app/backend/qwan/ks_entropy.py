def ks_entropy(lyapunov_spectrum):

    # KS = soma dos expoentes positivos
    return sum(l for l in lyapunov_spectrum if l > 0)
