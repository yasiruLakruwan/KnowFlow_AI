from .loader_base import DocumentLoader
import pypdf

# Create pdf loader using inheritance....

class PdfLoader(DocumentLoader):
    def __init__(self,file_path):
        self.file_path = file_path

    def load(self):
        reader = pypdf.PdfReader(self.file_path)
        text = " "
        for page in reader.pages:
            text += page.extract_text()
        return text
    
