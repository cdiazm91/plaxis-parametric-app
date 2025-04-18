from fpdf import FPDF
import tempfile
import os

def generate_pdf_report(tipo_suelo, espesor, estructura, resultados):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título
    pdf.set_font("Arial", "B", 16)
    pdf.cell(200, 10, "Informe de Diseño Paramétrico Geotécnico", ln=True, align="C")
    pdf.ln(10)

    # Parámetros del modelo
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Parámetros del Modelo:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(200, 10, f"Tipo de suelo: {tipo_suelo}", ln=True)
    pdf.cell(200, 10, f"Espesor de capa: {espesor} m", ln=True)
    pdf.cell(200, 10, f"Estructura de contención: {estructura}", ln=True)
    pdf.ln(10)

    # Resultados
    pdf.set_font("Arial", "B", 12)
    pdf.cell(200, 10, "Resultados del modelo:", ln=True)
    pdf.set_font("Arial", size=12)
    for key, value in resultados.items():
        pdf.cell(200, 10, f"{key}: {value}", ln=True)

    # Guardar archivo temporal
    temp_path = tempfile.NamedTemporaryFile(delete=False, suffix=".pdf").name
    pdf.output(temp_path)
    return temp_path
