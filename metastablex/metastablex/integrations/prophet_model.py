from prophet import Prophet
import pandas as pd

def run_prophet(df, municipio):

    sub = df[df["municipio"] == municipio].copy()

    df_prophet = pd.DataFrame({
        "ds": pd.to_datetime(sub["data"]),
        "y": sub["taxa"]
    })

    model = Prophet()
    model.fit(df_prophet)

    future = model.make_future_dataframe(periods=12, freq="M")
    forecast = model.predict(future)

    return forecast, model
