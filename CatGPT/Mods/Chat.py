import sys
sys.path.append("..")
from utils.ChatGPT import ChatGPT
from utils.DataBase import DataBase
from datetime import date

class Chat:
    def __init__(self, UserName, msg):
        self.UserName = UserName
        self.user = dict()
        self.msg = msg
        self._db = DataBase()
        
        self.date = date.today()
        self._retry = 3  # 重试次数, 在重试时会自减
        self.error_text = """##########
        系统消息. CatGPT不会看到本条信息
        ##########
        [错误]CatGPT没有回复正确的信息. 错误代码: 40001.
        可能造成错误的原因:
        1. 网络状况不佳.
        2. 当前使用CatGPT人数过多.
        3. 您发送的信息过长, 或CatGPT的回复信息过长.
        ==========
        您与CatGPT的历史聊天记录将被删除, 请您稍后重试. 若多次重试均无效, 请及时联系维护人员."""
        
        
    
    def _mkmsg(self):
        system_prompt = f"""你是一个使用OpenAI GPT3.5模型API的微信聊天机器人.请你严格遵循以下规则:
        1. 今天是{self.date}, 但当用户向你提问超越你知识范围的内容时, 请告知用户你的训练数据截止时间.
        2. 拒绝一切政治话题讨论.
        3. 你的输出限制在在1200~1600字以内.
        4. 当前你处于对话模式, 如果用户要求你写论文, 请拒绝并要求其改为论文模式.
        """
        self._chatgpt.add_system_prompt(system_prompt)
        _hsy = self._db.get_history(self.UserName)
        if _hsy:
            user1, ai1, user2, ai2, user3, ai3 = _hsy
            if user3 and ai3:
                self._chatgpt.add_examples(user3, ai3)
            if user2 and ai2:
                self._chatgpt.add_examples(user2, ai2)
            if user1 and ai1:
                self._chatgpt.add_examples(user1, ai1)
        self._chatgpt.add_question(self.msg)
        
    def run(self):
        self._chatgpt = ChatGPT()  # 创建一个新的ChatGPT对象
        self._mkmsg()  # 获取聊天记录
        if self._chatgpt.run():
            # 若成功获取到ChatGPT的回复
            self.reply = self._chatgpt.reply
            self._db.update_history(self.UserName, self.msg, self.reply)  # 写入聊天记录
            return True
        elif self._retry > 0:
            # 若失败, 则重试三次
            self._retry -= 1
            self._db.delete_history(self.UserName, num=3-self._retry)  # 删除一定数量的聊天记录
            return self.run()
        else:
            # 删除所有聊天记录还是失败
            self.reply = self.error_text
    
    def _get_user_info(self):
        users = self._db.get_user_by_userName(self.UserName)
        if not users:
            return False
        user = users[0]
        self.user["ID"] = user[0]
        self.user["UserName"] = user[1]
        self.user["UserType"] = user[2]
        self.user["TotalTokens"] = user[3]
        self.user["Day"] = user[4]
        self.user["Mod"] = user[5]
    

if __name__ == '__main__':
    print("Testing: Mods.Chat.py")
    c = Chat("yusijin", "请问我问的上一个问题是什么")
    print(c.run())
    print(c.reply)