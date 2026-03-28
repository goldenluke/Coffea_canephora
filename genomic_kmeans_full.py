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
parser.add_argument("--k", type=int, default=None)  # automático se None
parser.add_argument("--window", type=int, default=500)
parser.add_argument("--kmer", type=int, default=3)
parser.add_argument("--max_k", type=int, default=10)

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
    return [
        seq[i:i+tamanho]
        for i in range(0, len(seq), tamanho)
        if len(seq[i:i+tamanho]) == tamanho
    ]

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
# 4. ELBOW AUTOMÁTICO
# =====================================
def escolher_k(X, max_k):
    inertia = []
    K = range(1, max_k + 1)

    for k in K:
        model = KMeans(n_clusters=k, random_state=42, n_init=10)
        model.fit(X)
        inertia.append(model.inertia_)

    # heurística simples: maior queda relativa
    diffs = np.diff(inertia)
    ratio = diffs[1:] / diffs[:-1]

    k_escolhido = np.argmin(ratio) + 2

    plt.figure()
    plt.plot(K, inertia, marker='o')
    plt.title(f"Elbow (k escolhido ≈ {k_escolhido})")
    plt.xlabel("K")
    plt.ylabel("Inércia")
    plt.grid()
    plt.show()

    return k_escolhido

# =====================================
# PIPELINE
# =====================================
seqs_raw = ler_fasta(args.fasta)

# janelas
janelas = []
for seq in seqs_raw:
    janelas.extend(dividir_janelas(seq, args.window))

print(f"Total de janelas: {len(janelas)}")

# features
df = extrair_features(janelas, args.kmer)

print("Shape features:", df.shape)

# normalização
scaler = StandardScaler()
X_scaled = scaler.fit_transform(df)

# =====================================
# ESCOLHER K
# =====================================
if args.k is None:
    k_final = escolher_k(X_scaled, args.max_k)
else:
    k_final = args.k

print(f"\nK final: {k_final}")

# =====================================
# KMEANS
# =====================================
kmeans = KMeans(n_clusters=k_final, random_state=42, n_init=10)
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
# TRANSIÇÕES
# =====================================
transicoes_idx = []

for i in range(1, len(clusters)):
    if clusters[i] != clusters[i-1]:
        transicoes_idx.append(i)

print(f"Transições detectadas: {len(transicoes_idx)}")

# =====================================
# SCORE DE INSTABILIDADE
# =====================================
instabilidade = np.zeros(len(clusters))

for t in transicoes_idx:
    instabilidade[t] = 1

window = 50
instabilidade_suavizada = np.convolve(
    instabilidade,
    np.ones(window)/window,
    mode="same"
)

df["instabilidade"] = instabilidade_suavizada

# =====================================
# REGIÕES CRÍTICAS
# =====================================
threshold = np.percentile(instabilidade_suavizada, 95)

df["regiao_critica"] = df["instabilidade"] > threshold

print(f"Regiões críticas detectadas: {df['regiao_critica'].sum()}")

# =====================================
# VISUALIZAÇÕES
# =====================================

# PCA
plt.figure()
plt.scatter(df["pca1"], df["pca2"], c=df["cluster"])
plt.title("Clusters genômicos (PCA)")
plt.xlabel("PCA1")
plt.ylabel("PCA2")
plt.grid()
plt.show()

# clusters discretos
plt.figure(figsize=(15,4))
plt.scatter(range(len(df)), df["cluster"], s=1)
plt.title("Clusters ao longo do genoma")
plt.xlabel("Janela")
plt.ylabel("Cluster")
plt.grid()
plt.show()

# mapa linear
plt.figure(figsize=(15,3))
for i in range(len(df)):
    plt.axvspan(i, i+1, ymin=0, ymax=1,
                color=plt.cm.tab10(df["cluster"].iloc[i]))
plt.title("Mapa de estados do genoma")
plt.yticks([])
plt.xlabel("Janela")
plt.show()

# transições
plt.figure(figsize=(15,4))
plt.plot(clusters, linewidth=0.5)

for t in transicoes_idx:
    plt.axvline(t, alpha=0.05)

plt.title("Transições de estado")
plt.xlabel("Janela")
plt.ylabel("Cluster")
plt.show()

# instabilidade
plt.figure(figsize=(15,4))
plt.plot(instabilidade_suavizada)
plt.axhline(threshold)
plt.title("Instabilidade genômica")
plt.xlabel("Janela")
plt.ylabel("Score")
plt.show()

# regiões críticas
plt.figure(figsize=(15,4))
plt.plot(instabilidade_suavizada)

for i in range(len(df)):
    if df["regiao_critica"].iloc[i]:
        plt.axvspan(i, i+1, color='red', alpha=0.2)

plt.title("Regiões críticas")
plt.xlabel("Janela")
plt.ylabel("Instabilidade")
plt.show()

# =====================================
# POSIÇÃO GENÔMICA
# =====================================
df["posicao_inicio"] = df.index * args.window
df["posicao_fim"] = df["posicao_inicio"] + args.window

# =====================================
# EXPORTAÇÃO
# =====================================
df.to_csv("genomic_analysis.csv", index=False)

print("\n✅ Pipeline completo finalizado!")