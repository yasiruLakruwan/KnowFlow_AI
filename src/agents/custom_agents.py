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
    - answer directly

    Return ONLY one action
    """
        return self.llm.invoke(prompt).content.strip().lower()
    
    def critique(self,question,context,answer):
        prompt =f"""
    You are a strict evaluator.

    Question:
    {question}

    Context:
    {context}

    Answer:
    {answer}

    Is the answer:
    - grounded in the context?
    - relevent?
    - complete?

    Response ONLY with PASS or FAIL.
    """
        return self.llm.invoke(prompt).content.strip()
    
    