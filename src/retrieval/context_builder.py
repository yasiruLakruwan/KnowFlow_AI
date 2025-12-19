## Here we write context builder for the retriever documents.
from typing import List
from langchain_classic.schema import Document


class ContextBuilder:
    def __init__(self,max_tokens:int=3000):
        self.max_tokens = max_tokens
    
    def _estimate_tokens(self,text:str) -> int:
        # Simple approximation (good inough for now)
        return len(text.split())
    
    def build(self,docs:List[Document]) -> str:
        """
        Build LLM ready context from reranked documents.
        """
                