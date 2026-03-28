import pandas as pd
import numpy as np

print("📊 loading...")
df = pd.read_csv("genomic_metastablex.csv")

# =========================
# HOTSPOTS
# =========================
hotspots = df[df["hotspot"] == 1]

print("🔥 total hotspots:", len(hotspots))

# =========================
# BASIC STATS
# =========================
mean_risk = df["risk"].mean()
std_risk = df["risk"].std()

hotspots["zscore"] = (hotspots["risk"] - mean_risk) / std_risk

# =========================
# TOP HOTSPOTS
# =========================
top = hotspots.sort_values("risk", ascending=False).head(50)
top.to_csv("top_hotspots.csv", index=False)

print("🏆 top hotspots saved")

# =========================
# REGION CLASSIFICATION
# =========================
def classify(r):
    if r > 0.8:
        return "CRITICAL"
    elif r > 0.5:
        return "HIGH"
    elif r > 0.3:
        return "MODERATE"
    else:
        return "LOW"

df["risk_class"] = df["risk"].apply(classify)

# =========================
# DISTRIBUTION
# =========================
dist = df["risk_class"].value_counts()
print("\n📊 risk distribution:")
print(dist)

# =========================
# SPATIAL CLUSTERING
# =========================
clusters = []
current = []

for i,row in df.iterrows():
    if row.hotspot == 1:
        current.append(row.pos)
    else:
        if current:
            clusters.append((min(current), max(current)))
            current = []

print("\n🧬 hotspot clusters:", len(clusters))

# =========================
# SAVE CLUSTERS
# =========================
with open("hotspot_clusters.bed","w") as f:
    for s,e in clusters:
        f.write(f"chr1\t{int(s)}\t{int(e)}\tCLUSTER\n")

# =========================
# SUMMARY METRICS
# =========================
coverage = len(hotspots)/len(df)

print("\n📈 coverage:", coverage)
print("📈 mean hotspot risk:", hotspots["risk"].mean())

print("\n🚀 ANALYSIS COMPLETE")
