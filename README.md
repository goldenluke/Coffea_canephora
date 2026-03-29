# 🧬 MetastableX — Structural Genomics as a Metastable System

A systems-level pipeline for analyzing genomic sequences as continuous structural trajectories, integrating sequence-derived features, dynamical systems modeling, and epigenetic data.

---

## 📖 Overview

Traditional genomics focuses on discrete elements such as genes and regulatory regions.

MetastableX introduces a complementary perspective:

> The genome behaves as a **continuous structured system**, governed by constraints, transitions, and metastable dynamics.

This pipeline models genomic sequences as trajectories in a feature space, enabling the detection of structural transitions and their relationship with epigenetic signals.

---

## 🧠 Core Idea

Given a genomic sequence:

```

S = {s₁, s₂, ..., sₙ}, where sᵢ ∈ {A, T, C, G}

```

We segment it into windows:

```

Sⱼ ⊂ S, |Sⱼ| = w

```

Extract features:

```

GC(Sⱼ) = (n_G + n_C) / w
H(Sⱼ) = -∑ pₖ log₂(pₖ + ε)
C(Sⱼ) = |Σ(Sⱼ)| / w

```

Project into low dimension:

```

X' = (X - μ)W

```

Define structural signal:

```

f(j) = PC1

```

Smooth:

```

f_s(j) = ∑ f(i) Gσ(j - i)

```

Metastable risk:

```

R(j) = |df_s(j)/dj|

```

Normalized:

```

R̂(j) ∈ [0,1]

````

---

## 🔬 What This Pipeline Does

- Retrieves genes automatically from Ensembl
- Extracts genomic regions from GRCh38
- Computes structural features (GC, entropy, complexity)
- Projects features using PCA
- Builds a continuous structural signal
- Computes metastable risk (structural transitions)
- Detects hotspots
- Integrates DNase (ENCODE / UCSC)
- Performs statistical enrichment tests
- Generates plots per gene
- Exports results as CSV
- Supports batch multi-gene analysis via CLI

---

## ⚙️ Installation

```bash
git clone https://github.com/goldenluke/Coffea_canephora.git
cd Coffea_canephora

pip install numpy matplotlib scipy scikit-learn requests
````

---

## 🚀 Basic Usage

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

## 🧪 Example Output

```
🧬 TP53
hotspots: 8
overlap: 5
p-value: 0.017
SIGNIFICANT: True
```

---

## 📊 Outputs

### Per gene plots

Saved in:

```
plots/<GENE>.png
```

Includes:

* Metastable risk signal
* DNase regions overlay

---

### CSV summary

```
results.csv
```

Columns:

| gene | hotspots | overlap | pvalue | significant |
| ---- | -------- | ------- | ------ | ----------- |

---

## 🔁 Batch Mode (Key Feature)

The pipeline supports multi-gene execution using argparse:

```bash
python metastablex_paper_pipeline.py \
  --genes HBB TP53 BRCA1 MYC
```

This will:

* Fetch each gene automatically
* Run full analysis independently
* Generate plots per gene
* Aggregate results into one CSV

---

## 🧬 Epigenetic Integration

DNase hypersensitivity clusters are:

* downloaded automatically
* parsed from UCSC
* mapped to genomic windows

This allows:

> direct comparison between structural transitions and chromatin accessibility

---

## 📉 Statistical Test

Binomial test:

```
H0: overlap is random
H1: enrichment exists
```

```
p = (# DNase windows) / (total windows)
```

---

## 🔬 Interpretation

The pipeline does **not detect genes directly**.

Instead, it captures:

* structural constraints
* transition dynamics
* metastable organization

---

## 📊 Observed Behavior

Across multiple genes:

* Some show no enrichment (HBB, BRCA1)
* Some show significant overlap (TP53)
* Some show low structural variance (MYC)

---

## 🧠 Key Insight

> Metastable risk is **not universally aligned with function**, but may reveal **locus-specific structural regimes**

---

## 🌊 Multiscale Extension

Includes wavelet analysis:

* detects long-range structure
* reveals low-frequency dominance
* suggests hierarchical organization

---

## 🔄 Null Model

Supports shuffled genome comparison:

* preserves nucleotide composition
* destroys structure

Result:

> real genomes show reduced instability

---

## 🧬 Project Evolution

### Phase 1 — Coffee genome

Exploration in *Coffea canephora*

---

### Phase 2 — Structural modeling

Sliding windows + PCA

---

### Phase 3 — Metastable risk

Gradient-based transition metric

---

### Phase 4 — Null validation

Real vs shuffled genomes

---

### Phase 5 — Cross-species

* E. coli
* Arabidopsis
* Coffee

---

### Phase 6 — Human genome

HBB (sickle cell anemia)

Result:

> no enrichment

---

### Phase 7 — ENCODE integration

DNase overlap

---

### Phase 8 — Multi-gene analysis

Batch execution via argparse

---

## 🧪 Advanced Usage

### Large gene panel

```bash
python metastablex_paper_pipeline.py \
  --genes TP53 BRCA1 BRCA2 EGFR MYC KRAS PTEN
```

---

### High-resolution analysis

```bash
--window 500
```

---

### Broad context analysis

```bash
--flank 500000
```

---

### Combine everything

```bash
python metastablex_paper_pipeline.py \
  --genes TP53 BRCA1 MYC \
  --window 800 \
  --flank 300000
```

---

## ⚠️ Limitations

* PCA is linear
* window size sensitivity
* feature simplicity
* DNase dataset variability
* no direct functional validation

---

## 🔮 Future Work

* Hi-C integration (TADs)
* ATAC-seq validation
* nonlinear embeddings (UMAP, autoencoders)
* gene vs intergenic comparison
* multi-scale modeling

---

## 🧠 Scientific Position

MetastableX does not replace classical genomics.

It introduces a new perspective:

> genomic organization emerges from structural constraints and metastable dynamics

---

## 👨‍🔬 Author

Lucas Amaral Dourado

---

## 📜 License

MIT License

---

## 🚀 Final Note

This project evolved from exploratory analysis in coffee genomes to structural modeling and epigenetic integration in the human genome.

The key conclusion:

> the genome is not just a collection of genes, but a structured dynamical system operating under metastable constraints.

