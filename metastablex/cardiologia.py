import numpy as np
import matplotlib.pyplot as plt

# -------------------------------
# PARAMETERS
# -------------------------------

T = 2000           # number of beats
dt = 0.01

# baseline heart rate
HR0 = 70           # beats per minute

# physiological controls
alpha = 0.6        # stability term
beta = 0.4         # variability coupling
noise_strength = 0.02

# -------------------------------
# INITIALIZATION
# -------------------------------

hr = np.zeros(T)
hr[0] = HR0

sympathetic = np.zeros(T)
parasympathetic = np.zeros(T)

# -------------------------------
# DYNAMICS
# -------------------------------

for t in range(1, T):

    # autonomic nervous system fluctuations
    sympathetic[t] = 0.95 * sympathetic[t-1] + np.random.normal(0, 0.1)
    parasympathetic[t] = 0.95 * parasympathetic[t-1] + np.random.normal(0, 0.1)

    autonomic_balance = sympathetic[t] - parasympathetic[t]

    # meta-stable heart dynamics
    dhr = (
        -alpha * (hr[t-1] - HR0)     # attraction to baseline
        + beta * autonomic_balance   # physiological variability
        + noise_strength * np.random.randn()
    )

    hr[t] = hr[t-1] + dhr

# -------------------------------
# RR INTERVALS
# -------------------------------

rr = 60 / hr

# -------------------------------
# PLOTS
# -------------------------------

plt.figure(figsize=(12,5))

plt.subplot(1,2,1)
plt.plot(hr)
plt.title("Simulated Heart Rate Dynamics")
plt.xlabel("Time (beats)")
plt.ylabel("Heart Rate (BPM)")

plt.subplot(1,2,2)
plt.plot(rr)
plt.title("Simulated RR Interval Variability")
plt.xlabel("Time")
plt.ylabel("RR interval (s)")

plt.tight_layout()
plt.show()
