import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse
import math

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from sklearn.ensemble import RandomForestClassifier
from collections import Counter
from scipy.ndimage import gaussian_filter1d

# =====================================
# ARGUMENTOS
# =====================================
parser = argparse.ArgumentParser()
parser.add_argument("--fasta", required=True)
parser.add_argument("--window", type=int, default=2000)
parser.add_argument("--k", type=int, default=3)
parser.add_argument("--kmer", type=int, default=3)

args = parser.parse_args()

# =====================================
# FASTA
# =====================================
def ler_fasta(path):
    seqs = []
    with open(path, "r") as f:
        seq = ""
        for linha in f:
            linha = linha.strip()
            if linha.startswith(">"):
                if seq:
                    seqs.append(seq)
                    seq = ""
            else:
                seq += linha.upper()
        if seq:
            seqs.append(seq)
    return seqs

# =====================================
# JANELAS
# =====================================
def dividir_janelas(seq, tamanho):
    return [
        seq[i:i+tamanho]
        for i in range(0, len(seq), tamanho)
        if len(seq[i:i+tamanho]) == tamanho
    ]

# =====================================
# FEATURES BIOLÓGICAS
# =====================================
def gc_content(seq):
    return (seq.count("G") + seq.count("C")) / len(seq)

def shannon_entropy(seq):
    counts = Counter(seq)
    total = len(seq)
    return -sum((v/total) * math.log2(v/total) for v in counts.values())

def lz_complexity(seq):
    i, sub, complexity = 0, set(), 0
    while i < len(seq):
        for j in range(i+1, len(seq)+1):
            if seq[i:j] not in sub:
                sub.add(seq[i:j])
                complexity += 1
                break
        i = j
    return complexity / len(seq)

def gerar_kmers(seq, k):
    return [seq[i:i+k] for i in range(len(seq)-k+1)]

def kmer_features(seq, k):
    kmers = gerar_kmers(seq, k)
    cont = Counter(kmers)
    total = sum(cont.values())
    return {k: v/total for k, v in cont.items()}

# =====================================
# EXTRAÇÃO
# =====================================
def extrair_features(seqs, k):
    lista = []
    for seq in seqs:
        feat = {}
        feat.update(kmer_features(seq, k))
        feat["gc"] = gc_content(seq)
        feat["entropy"] = shannon_entropy(seq)
        feat["complexity"] = lz_complexity(seq)
        lista.append(feat)
    return pd.DataFrame(lista).fillna(0)

# =====================================
# PIPELINE
# =====================================
seqs_raw = ler_fasta(args.fasta)

janelas = []
for seq in seqs_raw:
    janelas.extend(dividir_janelas(seq, args.window))

df = extrair_features(janelas, args.kmer)

# NORMALIZAÇÃO
scaler = StandardScaler()
X = scaler.fit_transform(df)

# =====================================
# CLUSTER
# =====================================
kmeans = KMeans(n_clusters=args.k, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X)

clusters = gaussian_filter1d(clusters.astype(float), sigma=2)
clusters = np.round(clusters).astype(int)

df["cluster"] = clusters

# =====================================
# PCA
# =====================================
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X)
df["pca1"] = X_pca[:, 0]
df["pca2"] = X_pca[:, 1]

# =====================================
# INSTABILIDADE
# =====================================
trans = np.where(np.diff(clusters) != 0)[0]
inst = np.zeros(len(df))
inst[trans] = 1
inst = np.convolve(inst, np.ones(50)/50, mode="same")
df["instabilidade"] = inst

threshold = np.percentile(inst, 95)
df["critico"] = inst > threshold

# =====================================
# 🧬 DETECÇÃO DE REGIÕES CODIFICANTES
# =====================================
# heurística biológica simples
df["coding_score"] = (
    (df["gc"] * 0.4) +
    (df["entropy"] * 0.3) +
    (df["complexity"] * 0.3)
)

coding_threshold = df["coding_score"].quantile(0.75)
df["provavel_coding"] = df["coding_score"] > coding_threshold

# =====================================
# 🧠 CLASSIFICAÇÃO SUPERVISIONADA
# =====================================
features = df.drop(columns=["cluster", "pca1", "pca2", "critico", "provavel_coding"])

clf = RandomForestClassifier(n_estimators=100, random_state=42)
clf.fit(features, df["cluster"])

df["cluster_pred"] = clf.predict(features)

# importância das features
importances = pd.Series(clf.feature_importances_, index=features.columns)
print("\n🔥 IMPORTÂNCIA DAS FEATURES:")
print(importances.sort_values(ascending=False).head(10))

# =====================================
# 📊 EXPORTAR BED
# =====================================
df["start"] = df.index * args.window
df["end"] = df["start"] + args.window

bed = df[["start", "end", "cluster", "provavel_coding", "critico"]]
bed.columns = ["chromStart", "chromEnd", "cluster", "coding", "critical"]

bed.to_csv("genomic_regions.bed", sep="\t", index=False)

# =====================================
# VISUALIZAÇÕES
# =====================================

plt.figure()
plt.scatter(df["pca1"], df["pca2"], c=df["cluster"])
plt.title("PCA")
plt.show()

plt.figure(figsize=(15,4))
plt.plot(df["cluster"])
plt.title("Clusters")
plt.show()

plt.figure(figsize=(15,4))
plt.plot(df["instabilidade"])
plt.axhline(threshold)
plt.title("Instabilidade")
plt.show()

plt.figure(figsize=(15,4))
plt.plot(df["instabilidade"])

for i in range(len(df)):
    if df["critico"].iloc[i]:
        plt.axvspan(i, i+1, color='red', alpha=0.2)

plt.title("Regiões críticas")
plt.show()

plt.figure(figsize=(15,4))
plt.plot(df["coding_score"])
plt.axhline(coding_threshold)
plt.title("Regiões codificantes (heurística)")
plt.show()

# =====================================
# EXPORT FINAL
# =====================================
df.to_csv("genomic_full_analysis.csv", index=False)

print("\n✅ PIPELINE COMPLETO FINALIZADO")