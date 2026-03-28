import pandas as pd
import numpy as np
from math import comb

print("📊 loading data...")

df = pd.read_csv("genomic_metastablex.csv")

# =========================
# LOAD GFF
# =========================
def load_gff(path):
    genes = []
    with open(path) as f:
        for line in f:
            if line.startswith("#"):
                continue
            p = line.strip().split("\t")
            if len(p) > 4:
                genes.append((int(p[3]), int(p[4])))
    return genes

genes = load_gff("data/genes.gff")

print("🧬 genes loaded:", len(genes))

# =========================
# TOTAL GENOME COVERAGE BY GENES
# =========================
genome_size = df["pos"].max()

gene_bases = 0
for s,e in genes:
    gene_bases += (e - s)

gene_fraction = gene_bases / genome_size

print("📏 gene coverage fraction:", round(gene_fraction,4))

# =========================
# HOTSPOT OVERLAP
# =========================
def in_gene(pos):
    for s,e in genes:
        if s <= pos <= e:
            return True
    return False

df["in_gene"] = df["pos"].apply(in_gene)

hotspots = df[df["hotspot"] == 1]

k = hotspots["in_gene"].sum()   # successes
n = len(hotspots)              # trials
p = gene_fraction              # expected probability

print("\n🔥 hotspots total:", n)
print("🔥 hotspots in genes:", k)

observed_fraction = k / n if n > 0 else 0
print("📊 observed fraction:", round(observed_fraction,4))

# =========================
# BINOMIAL TEST (manual)
# =========================
def binomial_p_value(k, n, p):
    # P(X >= k)
    prob = 0
    for i in range(k, n+1):
        prob += comb(n,i) * (p**i) * ((1-p)**(n-i))
    return prob

p_value = binomial_p_value(k, n, p)

print("\n📉 p-value:", p_value)

# =========================
# INTERPRETAÇÃO
# =========================
print("\n🧠 INTERPRETATION:")

if p_value < 0.05:
    print("✅ Significant enrichment in genes")
elif p_value < 0.1:
    print("⚠️ Weak enrichment (trend)")
else:
    print("❌ No enrichment detected")

# =========================
# SAVE RESULTS
# =========================
result = {
    "hotspots_total": n,
    "hotspots_in_genes": int(k),
    "observed_fraction": observed_fraction,
    "expected_fraction": p,
    "p_value": p_value
}

pd.DataFrame([result]).to_csv("enrichment_results.csv", index=False)

print("\n💾 saved: enrichment_results.csv")
print("🚀 DONE")
