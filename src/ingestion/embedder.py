import os
import sys
from langchain_huggingface import HuggingFaceEmbeddings
from logging import getLogger
from utils.embeding_model import embeding_model,gemini_model

logger = getLogger(__name__)

# Srart Embeddings with chunks, metadata

class EmbeddingGenarater:

    def __init__(self,embed_model,gemini_model):
        self.embed_model = embed_model
        self.gem_model = gemini_model
    
    def embed_chunks(self,text:str):
        self.embed_model = embeding_model()
        self.gem_model = gemini_model()


