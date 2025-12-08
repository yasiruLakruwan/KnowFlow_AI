import os
from pdf_loader import PdfLoader
from loader_base import DocumentLoader
from config.path_config import presist_dir,data_dir
from text_cleaner import TextCleaner

class DirectryLoader(DocumentLoader):
    def __init__(self,directry_path):
        self.directry_path = directry_path

    def load(self):
        documents = []
        for file in os.listdir(self.directry_path):
            if file.lower().endswith(".pdf"):
                pdf_path = os.path.join(self.directry_path,file)
                loader = PdfLoader(pdf_path) 
                doc = loader.load()
                doc = TextCleaner.clean_text(doc)
                documents.append({
                    'filename':file,
                    'content': doc
                }) 
        return documents 
    

if __name__=="__main__":
    loader = DirectryLoader(data_dir)
    documents = loader.load()

    for index,item in enumerate(documents):
        if index<2 :
            print(f"----------Document--{index+1}--------")
            print(f"---------{item['filename']}---------------") 
            print(f"---------{item['content'][:200]}---------------") 

        



