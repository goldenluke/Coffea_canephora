import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import argparse

from sklearn.cluster import KMeans
from sklearn.preprocessing import StandardScaler
from sklearn.decomposition import PCA
from collections import Counter

# =====================================
# ARGUMENTOS
# =====================================
parser = argparse.ArgumentParser()
parser.add_argument("--fasta", required=True)
parser.add_argument("--k", type=int, default=5)
parser.add_argument("--window", type=int, default=500)
parser.add_argument("--kmer", type=int, default=3)

args = parser.parse_args()

# =====================================
# 1. LER FASTA
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
# 2. DIVIDIR EM JANELAS
# =====================================
def dividir_janelas(seq, tamanho):
    return [seq[i:i+tamanho] for i in range(0, len(seq), tamanho) if len(seq[i:i+tamanho]) == tamanho]

# =====================================
# 3. K-MERS
# =====================================
def gerar_kmers(seq, k):
    return [seq[i:i+k] for i in range(len(seq) - k + 1)]

def extrair_features(seqs, k):
    lista = []
    for seq in seqs:
        kmers = gerar_kmers(seq, k)
        cont = Counter(kmers)
        total = sum(cont.values())
        freq = {k: v/total for k, v in cont.items()}
        lista.append(freq)
    return pd.DataFrame(lista).fillna(0)

# =====================================
# PIPELINE
# =====================================
seqs_raw = ler_fasta(args.fasta)

# QUEBRAR EM JANELAS
janelas = []
for seq in seqs_raw:
    janelas.extend(dividir_janelas(seq, args.window))

print(f"Total de janelas: {len(janelas)}")

# FEATURES
df = extrair_features(janelas, args.kmer)

print("Shape features:", df.shape)

# NORMALIZAÇÃO
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

# =====================================
# ELBOW
# =====================================
inertia = []
k_range = range(1, 10)

for k in k_range:
    model = KMeans(n_clusters=k, random_state=42, n_init=10)
    model.fit(X_scaled)
    inertia.append(model.inertia_)

plt.figure()
plt.plot(k_range, inertia, marker='o')
plt.title("Elbow Method")
plt.xlabel("K")
plt.ylabel("Inércia")
plt.grid()
plt.show()

# =====================================
# KMEANS FINAL
# =====================================
kmeans = KMeans(n_clusters=args.k, random_state=42, n_init=10)
clusters = kmeans.fit_predict(X_scaled)

df["cluster"] = clusters

# =====================================
# PCA
# =====================================
pca = PCA(n_components=2)
X_pca = pca.fit_transform(X_scaled)

df["pca1"] = X_pca[:, 0]
df["pca2"] = X_pca[:, 1]

# =====================================
# TRANSIÇÕES (🔥 IMPORTANTE)
# =====================================
transicoes = 0
for i in range(1, len(clusters)):
    if clusters[i] != clusters[i-1]:
        transicoes += 1

print(f"\nClusters: {args.k}")
print(f"Transições detectadas: {transicoes}")

# =====================================
# VISUALIZAÇÃO PCA
# =====================================
plt.figure()
plt.scatter(df["pca1"], df["pca2"], c=df["cluster"])
plt.title("Clusters genômicos (PCA)")
plt.xlabel("PCA1")
plt.ylabel("PCA2")
plt.grid()
plt.show()

# =====================================
# SINAL AO LONGO DO GENOMA (🔥 MELHOR GRÁFICO)
# =====================================
plt.figure()
plt.plot(df["cluster"].values)
plt.title("Clusters ao longo do genoma")
plt.xlabel("Janela")
plt.ylabel("Cluster")
plt.grid()
plt.show()

# =====================================
# EXPORTAR
# =====================================
df.to_csv("resultado_genomico.csv", index=False)

print("\n✅ Finalizado!")