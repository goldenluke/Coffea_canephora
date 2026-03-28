def filtrar_covid(df):
    """
    CIDs relacionados à COVID:
    - U07.1 (confirmado)
    - U07.2 (suspeito)
    - B34.2 (coronavírus)
    """

    covid_cids = ["U071", "U072", "B342"]

    df["CID_PRINC"] = df["DIAG_PRINC"].str.replace(".", "")

    return df[df["CID_PRINC"].isin(covid_cids)]
