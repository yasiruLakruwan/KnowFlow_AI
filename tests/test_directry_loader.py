import os
from unittest.mock import patch
from src.ingestion.directry_loader import DirectryLoader
from fpdf import FPDF

def test_directry_loader():
    # 1. Setup the output directory
    output_directory = "two_pdfs_output"

    if not os.path.exists(output_directory):
        os.makedirs(output_directory)
        print(f"Created directory: {output_directory}")

    # --- File 1: Invoice.pdf ---
    file_name_1 = "Invoice.pdf"
    full_path_1 = os.path.join(output_directory, file_name_1)

    pdf1 = FPDF()
    pdf1.add_page()
    pdf1.set_font("Arial", size=16)
    pdf1.cell(200, 10, txt="Invoice Document", ln=True, align='C')
    pdf1.set_font("Arial", size=12)
    pdf1.cell(200, 10, txt="Details for the sale of goods.", ln=True)
    pdf1.output(full_path_1)
    print(f"Saved first file: {full_path_1}")


    # --- File 2: Report.pdf ---
    file_name_2 = "Report.pdf"
    full_path_2 = os.path.join(output_directory, file_name_2)

    pdf2 = FPDF()
    pdf2.add_page()
    pdf2.set_font("Courier", size=16)
    pdf2.cell(200, 10, txt="Quarterly Report Summary", ln=True, align='C')
    pdf2.set_font("Courier", size=10)
    pdf2.cell(200, 10, txt="Confidential data regarding Q3 performance.", ln=True)
    pdf2.output(full_path_2)
    print(f"Saved second file: {full_path_2}")



    