from DataBase import DataBase
from ChatGPT import ChatGPT
from datetime import date

class Chat:
    def __init__(self, UserName, msg):
        self.UserName = UserName
        self.msg = msg
        self._db = DataBase()
        self._chatgpt = ChatGPT()
        self.date = date.today()
        
    
    def mkmsg(self):
        system_prompt = f"""你是一个使用OpenAI GPT3.5模型API的微信聊天机器人.请你严格遵循以下规则:
        1. 今天是{self.date}, 但当用户向你提问超越你知识范围的内容时, 请告知用户你的训练数据截止时间.
        2. 拒绝一切政治话题讨论.
        3. 你的输出限制在在1200~1600字以内.
        4. 当前你处于对话模式, 如果用户要求你写论文, 请拒绝并要求其改为论文模式.
        """
        self._chatgpt.add_system_prompt(system_prompt)
        _hsy = self._db.get_history()
        if _hsy:
            user1, ai1, user2, ai2, user3, ai3 = _hsy
            if user3 and ai3:
                self._chatgpt.add_examples(user3, ai3)
            if user2 and ai2:
                self._chatgpt.add_examples(user2, ai2)
            if user1 and ai1:
                self._chatgpt.add_examples(user1, ai1)
        
        