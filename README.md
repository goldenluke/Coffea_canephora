# 🧬 MetastableX — Structural Genomics as a Metastable System

> A systems-level approach to understanding genomic organization as a continuous, constrained, and metastable trajectory in feature space.

---

## Overview

Traditional genomics has been highly successful in identifying genes, motifs, regulatory elements, and conserved regions. However, this piecewise view can miss a broader property of biological sequences: their **global structural organization**.

MetastableX explores a complementary idea:

> the genome can be modeled as a **continuous structured system**, not just as a list of discrete functional parts.

In this framework, a genome is treated as a trajectory through a structural feature space. Local sequence windows are converted into quantitative descriptors, projected into a lower-dimensional manifold, and analyzed as a dynamical system with transitions, stability zones, and metastable risk.

---

## Core Concept

Given a genomic sequence:

```text
S = {s₁, s₂, ..., sₙ},  where sᵢ ∈ {A, T, C, G}
```

We divide it into windows:

```text
Sⱼ ⊂ S,  |Sⱼ| = w
```

Compute features:

```text
GC(Sⱼ) = (n_G + n_C) / w
H(Sⱼ) = -∑ pₖ log₂(pₖ + ε)
C(Sⱼ) = |Σ(Sⱼ)| / w
```

Project:

```text
X' = (X - μ)W
```

Structural axis:

```text
f(j) = PC1
```

Smoothed signal:

```text
f_s(j) = ∑ f(i) Gσ(j - i)
```

Metastable risk:

```text
R(j) = |df_s(j)/dj|
```

Normalized:

```text
R̂(j) ∈ [0,1]
```

---

## Main Hypothesis

Genomes operate in a **metastable regime**, balancing:

- structural stability
    
- local flexibility
    
- constrained transitions
    

---

## Project History

### Phase 1 — Coffee genome

The project began with exploratory analysis of _Coffea canephora_, investigating whether genomic sequences exhibit global structure independent of functional annotation.

---

### Phase 2 — Formalization

Development of a reproducible pipeline:

- sliding windows
    
- feature extraction
    
- PCA projection
    
- structural manifold identification
    

---

### Phase 3 — Metastable risk

Definition of:

```text
R(j) = |df(j)/dj|
```

Interpreted as **structural transition intensity**.

---

### Phase 4 — Null model

Comparison with shuffled genomes:

- preserves composition
    
- destroys structure
    

Result:

> real genomes show reduced structural instability.

---

### Phase 5 — Cross-species validation

Applied to:

- _Escherichia coli_
    
- _Arabidopsis thaliana_
    
- _Coffea canephora_
    

Confirmed generality of structural constraints.

---

### Phase 6 — Human genome validation (HBB — sickle cell anemia)

The model was extended to the human genome (GRCh38), focusing on:

- Chromosome 11
    
- Gene **HBB (Hemoglobin Subunit Beta)**
    
- Associated with **sickle cell anemia**
    

#### Objective

Test whether metastable hotspots are enriched in functionally critical regions.

#### Result

- No overlap between hotspots and HBB region
    
- p-value ≈ 1.0
    
- No enrichment detected
    

#### Interpretation

This result suggests:

> metastable risk does **not** directly map to gene locations.

Instead:

- genes may reside in **structurally stable regions**
    
- metastability captures a **global structural property**
    
- structural transitions are **not gene-centric**
    

This is a key conceptual result of the project.

---

## Results Summary

### Structural manifold

Non-random distribution in feature space → constrained geometry.

---

### Structural axis

Smooth trajectory → continuity across genomic regions.

---

### Metastable risk

- lower in real genomes
    
- more organized than random
    

---

### Risk distribution

Shift toward lower values → structural suppression of instability.

---

### Structural memory

Autocorrelation indicates persistence across genomic distance.

---

### Frequency spectrum

Dominance of low frequencies → long-range organization.

---

### Multiscale structure (Wavelets)

Wavelet decomposition shows:

- energy concentrated at large scales
    
- absence of high-frequency noise
    

Suggests:

> hierarchical and possibly fractal-like organization.

---

## Interpretation

The genome behaves as:

- a constrained dynamical system
    
- not random
    
- not purely gene-driven
    

Metastability captures:

> the balance between order and flexibility in genomic structure.

---

## Biological Meaning

The model does **not** detect genes directly.

Instead, it reveals:

- structural constraints
    
- global organization
    
- emergent genomic behavior
    

---

## Why this matters

This approach bridges:

- bioinformatics
    
- information theory
    
- complex systems
    
- dynamical systems
    

---

## Repository Contents

Includes:

- PCA manifold plots
    
- structural axis
    
- metastable risk
    
- hotspot detection
    
- wavelet analysis
    
- human genome validation
    

---

## Installation

```bash
git clone https://github.com/goldenluke/metastablex.git
cd metastablex
pip install -r requirements.txt
```

---

## Usage

```bash
python pipeline.py --fasta genome.fa --window 1500
```

---

## Example (Human validation)

```bash
python metastablex_human_hbb.py
```

---

## Outputs

- pca.png
    
- structure.png
    
- risk.png
    
- distribution.png
    
- hotspots.png
    
- wavelet.png
    
- human_hbb.png
    
- figure_nature_final.png
    

---

## Limitations

- parameter sensitivity
    
- window size dependence
    
- linear PCA
    
- no direct functional validation
    
- epigenetic integration pending
    

---

## Future Directions

- DNase / ATAC-seq validation
    
- Hi-C (TAD boundaries)
    
- multiscale modeling
    
- nonlinear manifolds
    
- gene vs intergenic comparison
    

---

## Scientific Positioning

MetastableX does not replace classical genomics.

It introduces a new question:

> how does the genome behave as a structured system?

---

## License

MIT License

---

## Author

Lucas Amaral Dourado

---

## Final Note

This project evolved from exploratory analysis in coffee genomes to structural validation in the human genome.

The key insight:

> genomic organization cannot be fully explained by genes alone.

Instead, it reflects a deeper structural regime — metastability.
