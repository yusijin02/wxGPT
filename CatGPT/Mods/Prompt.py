import sys
sys.path.append("..")

import json
from utils.ChatGPT import ChatGPT
from utils.DataBase import DataBase
import content.text as TEXT

class Prompt:
    def __init__(self, userName, json):
        self.userName = userName
        self.json = json
        self._db = DataBase()
        self.user = dict()
        if not self._get_user_info():
            self._db.add_user(userName)
            self._get_user_info()
        
    
    def _get_user_info(self):
        users = self._db.get_user_by_userName(self.userName)
        if not users:
            return False
        user = users[0]
        self.user["ID"] = user[0]
        self.user["UserName"] = user[1]
        self.user["UserType"] = user[2]
        self.user["TotalTokens"] = user[3]
        self.user["Day"] = user[4]
        self.user["Mod"] = user[5]
    
    def _isAvailable(self):
        return False if self.user["userType"] == "Banned" else True
    
    def _json2dict(self):
        self._chatgpt = ChatGPT()
        try:
            _list = json.loads(self.json)
            for _dict in _list:
                if _dict["role"] == "system":
                    self._chatgpt.add_system_prompt(_dict["content"])
                elif _dict["role"] == "user":
                    self._chatgpt.add_question(_dict["content"])
                elif _dict["role"] == "assistant":
                    self._chatgpt.add_examples(_dict["content"])
            return True
        except:
            return False
    
    def run(self):
        if not self._isAvailable():
            self.reply = TEXT.Error_userBanned
            return False
        if not self._json2dict():
            self.reply = TEXT.Error_PromptMod_JsonError
            return False
        if not self._chatgpt.run():
            self.reply = TEXT.Error_ChatMod
            return False
        self.reply = self._chatgpt.reply
        return True
    

if __name__ == '__main__':
    print("Testing: Prompy.py")
    userName = "testUser"
    jsonstr = """[{"role": "system", "content": "你是猫猫"}, {"role": "user", "content": "介绍下你自己"}]"""
    prompt = Prompt(userName, jsonstr)
    print(prompt.run())
    print(prompt.reply)