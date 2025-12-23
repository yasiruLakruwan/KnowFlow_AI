class LlmClient:
    def __init__(self,llm_model):
        self.llm_model = llm_model

    def genarate(self,prompt:str) -> str:
        response = self.llm_model.invoke(prompt)

        # Normalize response
        if hasattr(response,"content"):
            return response.content.strip()
        
        return str(response).strip()
    

    