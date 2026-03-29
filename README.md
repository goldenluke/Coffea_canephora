# 🧬 MetastableX — Structural Genomics as a Metastable System

A systems-level platform for analyzing genomic sequences as continuous structural trajectories, integrating sequence-derived features, dynamical systems modeling, epigenetic data, and AI-driven interpretation.

---

## 📖 Overview

Traditional genomics focuses on discrete elements such as genes and regulatory regions.

MetastableX introduces a complementary perspective:

> The genome behaves as a **continuous structured system**, governed by constraints, transitions, and metastable dynamics.

This platform models genomic sequences as trajectories in a feature space, enabling the detection of structural transitions and their relationship with epigenetic signals.

---

## 🧠 Core Idea

Given a genomic sequence:

```
S = {s₁, s₂, ..., sₙ}, where sᵢ ∈ {A, T, C, G}
```

Segment into windows:

```
Sⱼ ⊂ S, |Sⱼ| = w
```

Extract features:

```
GC(Sⱼ) = (n_G + n_C) / w
H(Sⱼ) = -∑ pₖ log₂(pₖ + ε)
C(Sⱼ) = |Σ(Sⱼ)| / w
```

Projection:

```
X' = (X - μ)W
```

Structural signal:

```
f(j) = PC1
```

Metastable risk:

```
R(j) = |df_s(j)/dj|
```

---

## 🔬 What This Platform Does

- Retrieves genes automatically from Ensembl
- Extracts genomic sequences (GRCh38)
- Computes structural features (GC, entropy, complexity)
- Projects features via PCA
- Computes metastable risk
- Detects hotspots
- Integrates ENCODE DNase data
- Performs enrichment analysis
- Generates scientific plots
- Stores results in PostgreSQL (JSONB)
- Provides REST API (Django)
- Provides interactive UI (React + Plotly)
- Uses LLM (Llama) to interpret results
- Generates scientific text automatically

---

## ⚙️ Installation

```bash
git clone https://github.com/goldenluke/Coffea_canephora.git
cd Coffea_canephora

pip install numpy matplotlib scipy scikit-learn requests django djangorestframework psycopg2-binary
```

---

## 🚀 CLI Usage

### Single gene

```bash
python metastablex_paper_pipeline.py --genes HBB
```

---

### Multiple genes

```bash
python metastablex_paper_pipeline.py \
  --genes HBB TP53 BRCA1 MYC
```

---

### Custom parameters

```bash
python metastablex_paper_pipeline.py \
  --genes TP53 \
  --window 1500 \
  --flank 300000
```

---

## 🌐 Full Platform (Backend + Frontend)

### Start backend

```bash
cd metastablex_app/backend
python manage.py runserver
```

---

### Start frontend

```bash
cd metastablex_app/frontend
npm start
```

---

## 🔌 API Usage

### Run analysis

```bash
curl -X POST http://127.0.0.1:8000/api/run/ \
-H "Content-Type: application/json" \
-d '{"genes":["HBB","TP53"]}'
```

---

### Get history

```bash
curl http://127.0.0.1:8000/api/analyses/
```

---

### Generate paper section

```bash
curl -X POST http://127.0.0.1:8000/api/paper/ \
-H "Content-Type: application/json" \
-d '{"genes":["TP53","BRCA1"]}'
```

---

## 🧠 LLM Integration

MetastableX integrates Llama (via Ollama):

```bash
ollama run llama3
```

Used for:

- automatic interpretation
- scientific explanation
- paper generation

---

## 📊 Frontend Features

The React dashboard provides:

- Risk curves
- Smoothed signals
- Histograms
- CDF plots
- Boxplots
- Heatmaps
- Autocorrelation
- Frequency spectrum (FFT)
- PCA projection
- Hotspot visualization
- AI interpretation panel
- Automatic paper generation

---

## 🧪 Example Output

```
TP53
hotspots: 8
overlap: 5
p-value: 0.017
SIGNIFICANT: True
```

---

## 🧬 Epigenetic Integration

DNase hypersensitivity clusters:

- downloaded automatically from UCSC
- mapped to genomic windows
- compared against structural hotspots

---

## 📉 Statistical Test

Binomial test:

```
H0: overlap is random
H1: enrichment exists
```

---

## 🔁 Null Model

Randomized genome:

- preserves composition
- destroys structure

Result:

> real genomes show reduced instability

---

## 🧠 AI-Generated Science

The platform can generate:

- interpretation of results
- structured explanations
- full Results section of a paper

---

## 🧪 Advanced Usage

### Large gene panel

```bash
python metastablex_paper_pipeline.py \
  --genes TP53 BRCA1 BRCA2 EGFR MYC KRAS PTEN
```

---

### High-resolution

```bash
--window 500
```

---

### Large context

```bash
--flank 500000
```

---

### Combined

```bash
python metastablex_paper_pipeline.py \
  --genes TP53 BRCA1 MYC \
  --window 800 \
  --flank 300000
```

---

## 🧬 Project Evolution

1. Coffee genome exploration (*Coffea canephora*)
2. Structural modeling
3. Metastable risk formulation
4. Null validation
5. Cross-species validation
6. Human genome (HBB)
7. ENCODE integration
8. Multi-gene analysis
9. Full-stack platform (Django + React)
10. AI integration (Llama)
11. Automatic scientific writing

---

## ⚠️ Limitations

- PCA is linear
- window sensitivity
- simplified features
- DNase variability
- limited biological validation

---

## 🔮 Future Work

- Hi-C / TAD integration
- ATAC-seq validation
- UMAP / deep embeddings
- multi-scale wavelets
- gene vs intergenic modeling

---

## 🧠 Scientific Position

MetastableX does not replace classical genomics.

It introduces:

> a structural and dynamical perspective on genome organization

---

## 👨‍🔬 Author

Lucas Amaral Dourado

---

## 📜 License

MIT License

---

## 🚀 Final Note

This project evolved from exploratory analysis in coffee genomes to a full platform integrating structural genomics, epigenetics, and artificial intelligence.

> The genome is not just a sequence — it is a dynamical system.
