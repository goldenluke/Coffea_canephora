import numpy as np

def mfdfa(series, q_vals=None):

    if q_vals is None:
        q_vals = np.linspace(-5, 5, 21)

    series = np.array(series)
    N = len(series)

    # perfil acumulado
    profile = np.cumsum(series - np.mean(series))

    scales = np.logspace(1, np.log10(N/4), 20).astype(int)
    scales = np.unique(scales)

    Fq = []

    for q in q_vals:

        Fqs = []

        for s in scales:

            if s < 4:
                continue

            segments = N // s
            rms = []

            for v in range(segments):

                seg = profile[v*s:(v+1)*s]
                x = np.arange(s)

                # detrend linear
                p = np.polyfit(x, seg, 1)
                trend = np.polyval(p, x)

                rms.append(np.sqrt(np.mean((seg - trend)**2)))

            rms = np.array(rms)

            if q == 0:
                Fqs.append(np.exp(0.5 * np.mean(np.log(rms**2))))
            else:
                Fqs.append((np.mean(rms**q))**(1/q))

        Fq.append(Fqs)

    Fq = np.array(Fq)

    # h(q)
    hq = []
    for i in range(len(q_vals)):
        coeffs = np.polyfit(np.log(scales[:len(Fq[i])]), np.log(Fq[i]), 1)
        hq.append(coeffs[0])

    hq = np.array(hq)

    # τ(q)
    tau = q_vals * hq - 1

    # α e f(α)
    alpha = np.gradient(tau, q_vals)
    f_alpha = q_vals * alpha - tau

    return alpha, f_alpha
