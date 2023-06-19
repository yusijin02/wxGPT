from ChatGPT import ChatGPT

class Chat:
    def __init__(self, friendName):
        self.friendName = friendName
        self.chatgpt = ChatGPT()
        
    def _is_banned(self):
        pass