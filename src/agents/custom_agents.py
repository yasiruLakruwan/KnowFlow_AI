class CustomAgents:
    def __init__(self,llm):
        self.llm = llm
    def plan_aciton(self,quesiton,chat_history):
        prompt = f"""
    You are a RAG planner.

    Conversation history:
    {chat_history}
    User question:
    {quesiton}
    Deside the next action:
    - rewrite
    - rewrite and retrive
    - ask clarification
    - asswer directly

    Return ONLY one action
    """
        return self.llm.invoke(prompt).content.strip().lower()
    
    def critic(self,question,context,answer):
        pass