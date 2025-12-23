from src.answer_genaration.prompts import RAG_PROMPT
from src.answer_genaration.llm_client import LlmClient
from logger import get_logger
from utils.embeding_model import gemini_model
logger = get_logger(__name__)

class ResponseGenarater:
    def __init__(self):
        self.llm_client = None

    def genarate(self,query:str,context:str) ->str:
        prompt = RAG_PROMPT.format(
            context = context,
            question = query
        )
        llm_model = gemini_model()
        self.llm_client = LlmClient(llm_model)
        answer = self.llm_client.genarate(prompt)
        return answer