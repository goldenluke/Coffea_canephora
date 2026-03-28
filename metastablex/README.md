<h1 align="center">🧠 MetastableX</h1>
<h3 align="center">A Unified Computational Framework for Metastability, Critical Transitions, and Emergent Structure in Complex Systems</h3>

<p align="center">
A research-grade framework to simulate, measure, and interpret metastable dynamics across physical, epidemiological, and informational systems.
</p>

<p align="center">
⚙️ PyTorch • 📊 Time-Series • 🧠 Complex Systems • 🌊 Nonlinear Dynamics • 📐 Fractals • 🏥 Public Health • 🤖 AI
</p>

---

# 📄 Article

Full theoretical foundation:

https://goldenluke.github.io/metastablex/

---

# 📌 Abstract

Complex systems do not operate in equilibrium — they evolve through **metastable regimes**, where transient structures emerge, persist, and dissolve.

**MetastableX** is a computational framework designed to:

- simulate metastable field dynamics (QWAN)
- detect critical transitions
- quantify emergent structure
- measure instability and complexity
- forecast systemic behavior

The framework integrates:

- statistical physics (energy, entropy, criticality)
- nonlinear dynamics (Lyapunov, bifurcation, chaos)
- information theory (Shannon, permutation entropy)
- geometry (fractal dimension, interface roughness)
- machine learning (LSTM, clustering)
- epidemiology (DATASUS / SIH-SUS)
- AI interpretation (LLMs)

---

# 🧠 1. Conceptual Foundation

MetastableX treats systems as:

> **fields evolving under competing forces of order and instability**

Instead of static states, the framework models:

- continuous transformation
- transient organization
- regime transitions

---

# ⚙️ 2. Core Mathematical Model (QWAN)

## Field Evolution

$$
x_{t+1} = x + \Delta t (\nabla^2 x - x^3 + x)
$$

- diffusion (∇²x)
- nonlinear stabilization (-x³)
- growth term (+x)

---

## Energy

$$
\Phi = \langle x^2 \rangle
$$

Measures global activity intensity.

---

## Variance

$$
I = \langle (x - \mu)^2 \rangle
$$

Captures system fluctuations.

---

## Lyapunov (proxy)

$$
\lambda \approx \log(\mathrm{Var}(x))
$$

Approximates sensitivity to perturbations.

---

## KPZ (interface growth)

$$
W = \sqrt{\langle (h - \bar{h})^2 \rangle}
$$

Measures roughness of the field.

---

## Fractal Dimension

$$
D = \frac{\log N(\epsilon)}{\log(1/\epsilon)}
$$

Quantifies interface complexity.

---

# 🌊 3. Dynamical Systems Analysis

## 🔥 Chaos & Stability

- Lyapunov spectrum (multi-dimensional)
- detection of chaotic regimes

---

## 🧭 Bifurcation Analysis

- parameter scanning
- phase diagram generation
- regime transitions

---

## 🌀 Phase Space Reconstruction

- Takens embedding
- attractor reconstruction
- trajectory analysis

---

## 📐 Fractal & Multifractal Analysis

- box-counting dimension
- Kaplan–Yorke dimension
- multifractal spectrum

---

## 🔗 Correlation Dimension

Grassberger–Procaccia:

$$
C(r) \sim r^D
$$

---

## 🧠 Entropy Measures

- Shannon entropy  
- permutation entropy  
- Kolmogorov–Sinai approximation  

---

# 🧬 4. Structure & Emergence

## 🔷 Cluster Detection

- connected components
- metastable domains

---

## 🧭 Cluster Tracking

- persistent IDs
- trajectory tracking
- merging (coalescence)
- splitting (fission)

---

## 📏 Geometry

- perimeter
- roughness
- interface analysis

---

## 📈 Growth Dynamics

- domain growth velocity
- KPZ scaling behavior

---

## 🔥 Nucleation Detection

- automatic emergence of structure
- early phase transitions

---

# 📊 5. Time-Series Intelligence

## 📉 Early Warning Signals

- variance increase  
- autocorrelation increase  
- entropy peaks  

---

## 🤖 Machine Learning

- LSTM forecasting
- anomaly detection
- regime classification

---

## 🧠 Clustering

- temporal clustering of regimes
- automatic segmentation

---

# 🏥 6. Epidemiological Layer

## DATASUS Integration

- SIH/SUS ingestion
- multi-state, multi-year analysis
- municipality-level resolution

---

## 🦠 COVID Detection

- CID filtering (U07, B34)
- detection as phase transition

---

## 📊 Indicators

- hospitalization dynamics
- chronic disease burden
- regional clustering

---

## ⚙️ SIR + ML

$$
S \rightarrow I \rightarrow R
$$

Combined with ML for prediction and anomaly detection.

---

# 🤖 7. AI Interpretation Layer

## Local LLM (Ollama / Llama3)

- offline execution
- no external API

---

## Capabilities

- interpret metrics
- generate reports
- explain transitions
- translate dynamics into language

---

## Pipeline
data → physics → dynamics → structure → metrics → AI → interpretation


---

# 🧪 8. Simulation Engine

## QWAN (Quantum Wave Adaptive Network)

- metastable field dynamics
- emergent structure formation
- continuous evolution

---

## Features

- real-time simulation
- GPU acceleration (PyTorch)
- multi-instance QWAN
- scenario comparison

---

# 🎛 9. Interactive System

- real-time WebSocket simulation
- dashboard interface (React)
- glassmorphism UI
- live metrics visualization

---

## Visual Capabilities

- field rendering
- cluster visualization
- trajectories
- energy heatmaps
- bifurcation heatmaps

---

# 📦 Installation

```bash
pip install metastablex
```


# 🚀 Quick Example
```python
from metastablex import Simulation

sim = Simulation()

for _ in range(100):
    state = sim.step()

print(state["Phi"])
print(state["lyapunov"])
``` 
