from utils.DataBase import DataBase
from Mods.Chat import Chat


class ListeningMessages:
    def __init__(self, userName, mesgText, userType="friend"):
        self.userName = userName
        self.userType = userType
        self.mesgText = mesgText
        
        self._db = DataBase()
        self._setUser()
        if self.user is None:
            self.isNewUser = True
            self._addUser()
            self._setUser()
        else:
            self.isNewUser = False
        
    
    def _setUser(self):
        users = self._db.get_user_by_userName(self.userName)
        if users:
            user = users[0]
            _dict = dict()
            _dict["ID"] = user[0]
            _dict["userName"] = user[1]
            _dict["userType"] = user[2]
            _dict["totalTokens"] = user[3]
            _dict["day"] = user[4]
            _dict["mod"] = user[5]
            self.user = _dict
        else:
            self.user = None
            
    def _addUser(self):
        self._db.add_user(self.userName)
        
    
    def _isAvailable(self):
        return False if self.user["userType"] == "Banned" else True
    
    def run(self):
        if self.userType != "friend":
            self.user["mod"] = "Default"
        if not self._isAvailable():
            self.reply = self._mod_Banned()
        elif self.user["mod"] == "Chat":
            self.reply = self._mod_Chat()
        elif self.user["mod"] == "Default":
            self.reply = self._mod_Default()
    
    def _mod_Banned(self):
        return """##########
系统消息. CatGPT不会看到本条信息
##########
[错误]你的用户已停止使用CatGPT, 详情请联系维护人员."""
    
    def _mod_Chat(self):
        _chat = Chat(self.userName, self.mesgText)
        if _chat.run():
            return f"""##########
聊天模式
##########
{_chat.reply}"""
        else:
            return """##########
系统消息. CatGPT不会看到本条信息
##########
[错误]CatGPT没有回复正确的信息. 错误代码: 40002.
可能造成错误的原因:
1. 网络状况不佳.
2. 当前使用CatGPT人数过多.
3. 您发送的信息过长, 或CatGPT的回复信息过长.
==========
您与CatGPT的历史聊天记录将被删除, 请您稍后重试. 若多次重试均无效, 请及时联系维护人员."""
            
    def _mod_Default(self):
        _chat = Chat(self.userName, self.mesgText)
        if _chat.run():
            return _chat.reply
        else:
            return """##########
系统消息. CatGPT不会看到本条信息
##########
[错误]CatGPT没有回复正确的信息. 错误代码: 40002.
可能造成错误的原因:
1. 网络状况不佳.
2. 当前使用CatGPT人数过多.
3. 您发送的信息过长, 或CatGPT的回复信息过长.
==========
您与CatGPT的历史聊天记录将被删除, 请您稍后重试. 若多次重试均无效, 请及时联系维护人员."""           
    
class ListeningCommands:
    def __init__(self, userName, mesgText, userType="friend"):
        self.userName = userName
        self.mesgText = mesgText
        self._get_command()
        
    def _get_command(self):
        try:
            _list = self.mesgText.split(" ")
            self.command = _list[1]
        except:
            self.command = None


if __name__ == '__main__':
    window = ListeningMessages("testUser", "请介绍你自己")
    print(window.run())
    print(window.reply)