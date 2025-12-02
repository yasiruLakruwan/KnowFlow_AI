import os
from .pdf_loader import PdfLoader
from .loader_base import DocumentLoader
from config.path_config import presist_dir

class DirectryLoader(DocumentLoader):
    def __init__(self,directry_path):
        self.directry_path = directry_path

    def load(self):
        documents = []
        for file in os.listdir(self.directry_path):
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(self.directry_path,file)
                loader = PdfLoader(pdf_path)
                documents.append(loader.load()) 
        return documents