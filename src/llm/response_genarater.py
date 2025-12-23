from prompts import RAG_PROMPT
from llm_client import LlmClient
from logger import get_logger

logger = get_logger(__name__)

class ResponseGenarater:
    def __init__(self,llm):
        self.llm_client = LlmClient(llm)

    def genarate(self,query:str,context:str) ->str:
        prompt = RAG_PROMPT.format(
            context = context,
            question = query
        )

        answer = self.llm_client.genarate(prompt)
        return answer