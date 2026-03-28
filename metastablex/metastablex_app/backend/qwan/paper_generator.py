from reportlab.platypus import SimpleDocTemplate, Paragraph, Image
from reportlab.lib.styles import getSampleStyleSheet

def generate_paper():

    doc = SimpleDocTemplate("qwan_paper.pdf")
    styles = getSampleStyleSheet()

    elements = []

    elements.append(Paragraph("QWAN Dynamical System Analysis", styles["Title"]))
    elements.append(Paragraph("Automated report", styles["Normal"]))

    elements.append(Image("bifurcation_map.png", width=400, height=300))
    elements.append(Image("phase_diagram.png", width=400, height=300))

    doc.build(elements)

    return "qwan_paper.pdf"
