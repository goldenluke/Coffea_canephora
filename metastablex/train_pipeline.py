from metastablex.qwan.train import train_model

municipios = df["municipio"].unique()

model = train_model(df, municipios, device="cuda")
