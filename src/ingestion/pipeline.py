from directry_loader import DirectryLoader
from chunker import TextChunking
from embedder import EmbeddingGenarater
from config.path_config import *


def pipeline():
    # Directry loader
    loader = DirectryLoader(data_dir)
    documents = loader.load()

    for index,item in enumerate(documents):
        if index<2 :
            print(f"----------Document--{index+1}--------")
            print(f"filename---------{item['filename']}---------------") 
            print(f"content---------{item['content'][:500]}---------------")
    
    chunker = TextChunking(700,70)

    

if __name__=="__main__":
    pipeline() 

