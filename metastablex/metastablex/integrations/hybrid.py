from metastablex.qwan.runner import run_qwan

def run_hybrid(series, forecast):

    # histórico
    hist_res = run_qwan(series)

    # futuro previsto
    future_series = forecast["yhat"].values[-len(series):]

    fut_res = run_qwan(future_series)

    return {
        "historical": hist_res,
        "forecast": fut_res
    }

