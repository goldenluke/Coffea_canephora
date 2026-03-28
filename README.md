# 🧬 Coffea canephora Genomic Structural Analysis

![Python](https://img.shields.io/badge/python-3.10+-blue.svg)
![Status](https://img.shields.io/badge/status-research-orange)
![License](https://img.shields.io/badge/license-MIT-green)
![Domain](https://img.shields.io/badge/domain-bioinformatics-purple)

---

## 🧠 Overview

This project explores the **structural organization of genomic sequences** using a hybrid feature-based approach combined with unsupervised learning and dynamical analysis.

Instead of treating DNA as a static string, this pipeline models the genome as a **complex system**, revealing:

- Structural regimes (clusters)
- Continuous transitions between states
- Instability patterns
- Critical regions (hotspots)
- Potential coding-like regions (heuristic)

---

## 🔬 Key Idea

The genome is modeled as a **metastable system**, where:

- States correspond to structural regimes
- Transitions reflect local structural changes
- Instability identifies critical boundaries

This approach connects **bioinformatics with complex systems theory**.

---

## ⚙️ Methodology

### 📊 Feature Extraction

Each genomic window is transformed into a feature vector using:

- k-mer frequencies (k=3)
- GC content
- Shannon entropy
- Sequence complexity (Lempel-Ziv inspired)

---

### 🤖 Modeling

- KMeans clustering → structural regimes
- PCA → low-dimensional manifold
- Gaussian smoothing → denoising
- Instability metric → transition density
- Random Forest → feature importance

---

### 🧬 Biological Heuristics

Coding-like regions are inferred using:

- GC content
- Entropy
- Complexity

---

## 📈 Results Interpretation

The pipeline reveals:

- A **low-dimensional manifold** governing genomic structure
- **Three dominant structural regimes**
- **Continuous transitions** between states
- **Localized instability hotspots**
- A **multifactorial organization** driven by composition and diversity

---

## 🚀 Installation

```bash
git clone https://github.com/goldenluke/Coffea_canephora.git
cd Coffea_canephora
pip install -r requirements.txt
```

## ▶️ Usage

python genomic_full_pipeline.py --fasta your_sequence.fa --window 2000 --k 3

## ⚙️ Parameters

Parameter	Description
--fasta	Input FASTA file
--window	Window size (recommended: 2000–3000)
--k	Number of clusters
--kmer	k-mer size (default: 3)

## 📊 Outputs
## 📄 Files
genomic_full_analysis.csv → full dataset
genomic_regions.bed → genome browser file

## 📈 Visualizations
PCA (structural manifold)
Cluster distribution
Instability profile
Critical regions
Coding score signal

## 🧠 Example Insights
The genome is not homogeneous
Structure emerges from multiple interacting features
Instability highlights functional or structural boundaries

## 🧬 BED File Usage

Open in:

IGV (Integrative Genomics Viewer)
UCSC Genome Browser
🔥 Feature Importance

## Genomic structure is influenced by:

GC content
Entropy
Complexity
Specific k-mer patterns

This confirms a multifactorial organization.

## ⚠️ Limitations

Coding detection is heuristic (not ORF-based)
KMeans imposes hard clustering
No validation with real annotations yet

## 🚀 Future Work

ORF detection (biological validation)
Hidden Markov Models
Multi-genome comparison
Integration with GFF/GTF annotations
Interactive visualization dashboard

## 🧠 Conceptual Contribution

This project proposes that:

Genomic organization can be described as a metastable system, where structural states emerge from the interaction of compositional and informational features.

## 👨‍💻 Author

Lucas Dourado

Medicine student
Computational modeling enthusiast
Focus: complex systems, health data, and bioinformatics

## License
MIT

Star the repository
Share with others
Contribute improvements
📜 License

MIT License
