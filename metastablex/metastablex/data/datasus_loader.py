from pysus.online_data.SIH import SIH
import pandas as pd

def load_sih_data(uf="SP", year=2020, months=None):

    sih = SIH()

    if months is None:
        months = list(range(1, 13))

    dfs = []

    for m in months:
        try:
            files = sih.get_files(uf=uf, year=year, month=m)
            files = sih.download(files)
            df = sih.load(files)

            dfs.append(df)

        except Exception as e:
            print(f"Erro mês {m}: {e}")

    if dfs:
        return pd.concat(dfs, ignore_index=True)

    return pd.DataFrame()
