class ChatMemory():
    def __init__(self,max_terns = 5):
        self.max_terns = max_terns
        self.chat_history = []

    def user_messages(self,message:str):
        self.chat_history.append("user",message)
        self._trim()
    
    def add_ai_message(self,message:str):
        self.chat_history.append("assistane",message)
        self._trim()
    
    def get(self):
        return self.chat_history
    
    def _trim(self):
        # Keep only last N terns (user+assistant = 2 entries per turn)
        if len(self.chat_history)>self.max_terns*2:
            self.chat_history = self.chat_history[-self.max_terns * 2:] 
