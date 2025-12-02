from src.ingestion.pdf_loader import PdfLoader

def test_pdf_loader():
    loader = PdfLoader(r"D:\KnowFlow_AI\docs\MachineLearning-Lecture01.pdf")
    text = loader.load()

    assert isinstance(text,str)
    assert len(text) > 0