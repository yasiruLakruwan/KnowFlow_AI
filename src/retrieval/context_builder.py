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

        context_block = []
        total_tokens = 0
        seen_chunks = set()

        for idx,doc in enumerate(docs,start=1):
            content = doc.page_content.strip()

            # Duplication safeguard

            if content in seen_chunks:
                continue
            seen_chunks.add(content)

            tokens = self._estimate_tokens(content)
            
            if total_tokens + tokens > self.max_tokens:
                break
            
            source = doc.metadata.get("source","unknown")
            page = doc.metadata.get("page","N/A")
            section = doc.metadata.get("section","")

            header = f"[Chunk {idx} | source: {source} | Page: {page}"

            if section:
                header += f"| Section: {section}"
            header += "]"

            block = f"{header}\n{content}"

            context_block.append(block)
            total_tokens += tokens
            
        return "\n\n---\n\n".join(context_block)
        