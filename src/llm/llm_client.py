class LlmClient:
    def __init__(self,llm):
        self.llm = llm

    def genarate(self,prompt:str) -> str:
        response = self.llm.invoke(prompt)

        # Normalize response
        if hasattr(response,"content"):
            return response.content.strip()
        
        return str(response).strip()