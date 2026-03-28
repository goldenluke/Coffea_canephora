import matplotlib.pyplot as plt
from fpdf import FPDF

def generate_report(series, metrics, filename="report.pdf"):

    plt.figure(figsize=(8,4))
    plt.plot(series)
    plt.title("Time Series")
    plt.savefig("timeseries.png")
    plt.close()

    pdf = FPDF()
    pdf.add_page()

    pdf.set_font("Arial","B",16)
    pdf.cell(0,10,"MetastableX Analysis Report",ln=True)

    pdf.set_font("Arial","",12)

    for k,v in metrics.items():
        pdf.cell(0,8,f"{k}: {v}",ln=True)

    pdf.image("timeseries.png",x=10,y=60,w=180)

    pdf.output(filename)
