
# 🧬 MetastableX — Structural Genomics as a Metastable System

> A systems-level approach to understanding genomic organization as a continuous, constrained, and metastable trajectory in feature space.

---

## Overview

Traditional genomics has been highly successful in identifying genes, motifs, regulatory elements, and conserved regions. However, this piecewise view can miss a broader property of biological sequences: their **global structural organization**.

MetastableX explores a complementary idea:

> the genome can be modeled as a **continuous structured system**, not just as a list of discrete functional parts.

In this framework, a genome is treated as a trajectory through a structural feature space. Local sequence windows are converted into quantitative descriptors, projected into a lower-dimensional manifold, and analyzed as a dynamical system with transitions, stability zones, and metastable risk.

This repository contains the implementation of that idea, including:

- sliding-window feature extraction
- PCA-based structural projection
- metastable risk estimation
- null-model comparison by sequence shuffling
- publication-style figures
- comparative analysis across organisms

---

## Core Concept

Given a genomic sequence:

```text
S = {s₁, s₂, ..., sₙ},  where sᵢ ∈ {A, T, C, G}
```

we divide it into windows of fixed size:

```text
Sⱼ ⊂ S,  |Sⱼ| = w
```

For each window, we compute structural descriptors:

GC content:

```text
GC(Sⱼ) = (n_G + n_C) / w
```

Shannon entropy:

```text
H(Sⱼ) = -∑ pₖ log₂(pₖ + ε)
```

Symbolic complexity:

```text
C(Sⱼ) = |Σ(Sⱼ)| / w
```

These features define a vector:

```text
Xⱼ ∈ ℝ³
```

The vectors are projected with PCA:

```text
X' = (X - μ)W
```

The first principal component is interpreted as a **structural axis**:

```text
f(j) = PC1
```

After Gaussian smoothing:

```text
f_s(j) = ∑ f(i) Gσ(j - i)
```

we define the **metastable risk**:

```text
R(j) = |df_s(j)/dj|
```

and normalize it to:

```text
R̂(j) ∈ [0,1]
```

This yields a continuous measure of structural transition intensity along the genome.

---

## Main Hypothesis

The central hypothesis is:

> genomic sequences are not random; they operate in a constrained metastable regime, balancing structural stability and flexibility.

In practical terms, this means the genome should show:

* smooth structural trajectories
* non-random manifold geometry
* lower risk than shuffled controls
* long-range structural memory
* organized transitions rather than chaotic fluctuations

---

## Project History

### Phase 1 — Coffee genome

The project began with an exploratory analysis of the coffee genome, specifically *Coffea canephora*.

At that stage, the goal was simple: determine whether a genome could be treated as a structured signal rather than only as a collection of annotated loci.

The early question was:

> can a genome reveal global organization even before we ask what each gene does?

That first formulation was intentionally humble and experimental. The analysis was not yet fully formalized, but it already suggested that local sequence composition was not distributed randomly.

---

### Phase 2 — Formalization

The next step was to turn the intuition into a reproducible pipeline:

* split the sequence into windows
* extract local features
* standardize the features
* project them into a low-dimensional manifold
* interpret the first component as a structural axis

This step revealed something important: the points did not scatter uniformly in feature space. They formed a continuous curve-like structure, which we began to interpret as a genomic manifold.

---

### Phase 3 — Metastable risk

Once the structural axis was established, we defined the metastable risk as the magnitude of local structural change.

This made it possible to ask not only where the genome is located in feature space, but how quickly it moves through that space.

High risk means abrupt structural transition.

Low risk means continuity and relative stability.

---

### Phase 4 — Null model

To test whether the observed organization was real, we created a null model by shuffling the sequence.

The shuffled genome preserves overall nucleotide composition but destroys local order.

This allowed a direct comparison:

* real genome
* composition-preserving random control

The real genome consistently behaved as a constrained system rather than a random one.

---

### Phase 5 — Comparative validation

The pipeline was then tested on different organisms, including:

* *Escherichia coli*
* *Arabidopsis thaliana*
* the coffee genome

This made it possible to compare structurally simple and structurally complex systems, and to see how the method behaves across biological scales.

---

## Results Summary

### Structural manifold

The PCA projection shows that windows do not fill feature space uniformly. Instead, they lie along a curved, low-dimensional manifold.

This suggests:

* strong internal constraints
* non-linear dependence between features
* global organization beyond local composition

---

### Structural axis

The first principal component behaves like a continuous axis across the genome.

Its smoothness indicates:

* local correlation between neighboring windows
* continuity of structural states
* absence of purely random fluctuations

---

### Metastable risk

The metastable risk profile captures structural transitions along the sequence.

Across real genomes, the risk tends to be:

* smoother
* more regular
* less extreme than in shuffled controls

This supports the idea that genomic organization suppresses instability rather than amplifying it.

---

### Risk distribution

The distribution of risk values usually shifts toward lower values in the real genome compared to the shuffled control.

This suggests that:

* structural stability is not incidental
* the real genome occupies a more constrained regime
* randomization increases structural volatility

---

### Structural memory

Autocorrelation and cumulative-risk plots suggest that genomic structure is not only local but also persistent across distance.

That means the genome retains memory of prior structural states rather than behaving like independent random windows.

---

### Frequency spectrum

Fourier analysis shows that low-frequency components dominate the structural signal.

This is consistent with:

* long-range organization
* smooth transitions
* multiscale structure

---

### Feature correlations

The feature correlation matrix shows that some descriptors are strongly coupled while others remain largely independent.

This matters because it explains why PCA is effective: the genome lives in a constrained feature space with redundancy and structure.

---

## Interpretation

The overall interpretation is that the genome is not best described as a random string of bases, nor merely as a list of genes. It behaves more like a structured system that moves through a constrained space of possible configurations.

This is why the concept of metastability is useful here.

A metastable system is neither frozen nor chaotic. It stays between extremes:

* stable enough to preserve function
* flexible enough to vary and evolve

That is exactly the kind of behavior this pipeline is designed to detect.

---

## Biological Meaning

The analysis does not claim that every fluctuation in the genome is biologically functional. Rather, it suggests that the genome as a whole is not structurally neutral.

The patterns observed may reflect:

* physical constraints on DNA organization
* evolutionary pressure toward robustness
* multiscale genomic architecture
* sequence-level regularization of variability

This opens the door to a new way of thinking about sequence data: not just as annotation targets, but as dynamical objects with emergent structure.

---

## Why this matters

This approach offers a bridge between:

* bioinformatics
* information theory
* nonlinear dynamics
* complex systems

It provides a way to study genome organization even when annotation is incomplete, and it can be used as a comparative framework across organisms.

---

## Repository Contents

Typical outputs generated by the pipeline include:

* PCA manifold plot
* structural axis plot
* metastable risk profile
* risk distribution comparison
* delta risk plot
* autocorrelation plot
* heatmap of features
* feature correlation matrix
* frequency spectrum
* cumulative risk plot
* final publication-style multi-panel figure

---

## Installation

```bash
git clone https://github.com/your-username/metastablex.git
cd metastablex
pip install -r requirements.txt
```

---

## Requirements

Typical dependencies include:

* Python 3.10+
* numpy
* pandas
* matplotlib
* seaborn
* scipy
* scikit-learn

---

## Usage

Run the pipeline with a FASTA file:

```bash
python pipeline.py --fasta genome.fa --window 1500
```

If you want to use an annotated genome with GFF/GTF support, you can extend the pipeline to compare hotspots with gene coordinates.

---

## Example Workflow

```bash
python metastablex_full_plots.py
python update_figure_nature.py
python metastablex_final_full.py
```

The scripts generate figures in the `plots/` directory.

---

## Outputs

Generated outputs may include:

* `pca.png`
* `structure.png`
* `risk.png`
* `distribution.png`
* `delta.png`
* `autocorrelation.png`
* `heatmap.png`
* `correlation.png`
* `fft.png`
* `cumulative.png`
* `figure_nature_final.png`
* `figure_nature_final.pdf`

---

## Figure Narrative

The final multi-panel figure typically contains:

* **A)** Structural manifold
* **B)** Structural axis
* **C)** Metastable risk
* **D)** Risk distribution
* **E)** Structural difference and memory

Together, these panels show that the genome occupies a constrained structural manifold, follows a smooth axis, and exhibits reduced instability relative to a randomized control.

---

## Limitations

This is an exploratory framework and has several limitations:

* parameter sensitivity
* dependence on window size
* dependence on smoothing scale
* PCA is linear and may miss nonlinear geometry
* current complexity descriptors are intentionally simple
* biological validation still needs to be expanded

These limitations do not invalidate the approach; they define the next steps.

---

## Future Directions

Possible extensions include:

* nonlinear manifold learning
* multiscale decomposition
* gene/intergenic/CDS stratification
* enrichment analysis
* cross-species comparisons
* integration with epigenetic data
* integration with transcriptomic data
* publication-ready comparative benchmarks

---

## Scientific Positioning

MetastableX is not a replacement for classical genomics. It is a complementary view that asks a different question:

> not only what the genome contains, but how it behaves as a structured system.

That shift in perspective is the main contribution of the project.

---

## Citation

If you use this project or build upon it, please cite the repository and describe the method as a structural/metastable analysis of genomic sequences based on sliding-window features, PCA projection, and risk-based transition profiling.

---

## License

MIT License

---

## Author

Lucas Amaral Dourado

---

## Final note

This project began as an intuitive exploration in *Coffea canephora* and evolved into a broader framework for structural genomics.

At its core, it asks a simple question:

> how does a genome stay stable without becoming rigid, and flexible without becoming random?

```
