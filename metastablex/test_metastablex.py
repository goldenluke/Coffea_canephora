from metastablex.dynamics.critical_system import simulate_critical_system
from metastablex.core.analyze import analyze_timeseries
from metastablex.regimes.tipping import detect_tipping
from metastablex.reporting.report import generate_report

series = simulate_critical_system(3000,r=0.01)

metrics = analyze_timeseries(series)

tipping,score = detect_tipping(series)

print(metrics)
print("tipping points:",tipping[:10])

generate_report(series,metrics)
