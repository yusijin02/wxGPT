import sqlite3
from datetime import date

class DataBase:
    def __init__(self):
        self._path = "./db/user.db"

        self._tableName = "users"
        self._conn = sqlite3.connect(self._path)
        self._cursor = self._conn.cursor()
        
    def get_history(self, UserName):
        # 获取历史记录
        # Input: UserName, str, 用户名
        # Output: 长度为6的元组
        CMD = f"""SELECT user1, ai1, user2, ai2, user3, ai3 FROM {self._tableName} WHERE UserName = '{UserName}'"""
        data = self._fetch(CMD)
        return data
    
    def delete_history(self, UserName, num=1):
        # 删除历史记录
        # Input: UserName, str, 用户名
        # Input: num, int, default=1, 删除的历史记录条数
        # Output: None
        if num == 1:  # 删除一条历史记录
            CMD = f"""UPDATE {self._tableName} SET user3 = NULL, ai3 = NULL WHERE UserName = '{UserName}'"""
        elif num == 2:  # 删除两条历史记录
            CMD = f"""UPDATE {self._tableName} SET user2 = NULL, ai2 = NULL, user3 = NULL, ai3 = NULL 
            WHERE UserName = '{UserName}'"""
        else:  # 删除所有历史记录
            CMD = f"""UPDATE {self._tableName} SET user1 = NULL, ai1 = NULL, user2 = NULL, ai2 = NULL, user3 = NULL, ai3 = NULL 
            WHERE UserName = '{UserName}'"""
        self._fetch(CMD, "zero")
        
    def update_history(self, UserName, user, ai):
        # 更新历史记录
        # Input: UserName, str, 用户名
        # Input: user, str, 用户对话的内容
        # Input: ai, str, AI对话的内容
        # Output: None
        _hty = self.get_history(UserName)
        if not _hty:  # 如果没有历史记录, 容易产生bug
            return
        user1, ai1, user2, ai2 = _hty[0], _hty[1], _hty[2], _hty[3]
        CMD = f"""UPDATE {self._tableName} SET user1 = '{user}', ai1 = '{ai}', 
        user2 = '{user1}', ai2 = '{ai1}', user3 = '{user2}', ai3 = '{ai2}' WHERE UserName = '{UserName}'"""
        self._fetch(CMD, "zero")    
        
    def add_user(self, UserName):
        # 添加一个用户
        # Input: UserName, str, 用户名
        # Output: None
        day = date.today().day
        day = 30 if day == 31 else day
        UserType = "User"
        TotalToken = 0
        Mod = "Chat"
        CMD = f"""INSERT INTO {self._tableName} (UserName, UserType, TotalToken, Day, Mod, user1, ai1, user2, ai2, user3, ai3) VALUES 
        ('{UserName}', '{UserType}', {TotalToken}, {day}, '{Mod}', NULL, NULL, NULL, NULL, NULL, NULL)"""
        self._fetch(CMD, "zero")
    
    def update(self, ID, key, value):
        # 更新一行的部分值
        # Input: ID, int, 用户ID
        # Input: key, str, 需要更新的列名. 可选: ["day", "mod", "usertype"]
        # Input: value, int/str, 需要更新的值
        # Output: None
        if key == "day":
            CMD = f"""UPDATE {self._tableName} SET Day = {value} WHERE ID = {ID}"""
        elif key == "mod":
            CMD = f"""UPDATE {self._tableName} SET Mod = '{value}' WHERE ID = {ID}"""
        elif key == "usertype":
            CMD = f"""UPDATE {self._tableName} SET UserType = '{value}' WHERE ID = {ID}"""
        else:
            return
        self._fetch(CMD, "zero")
    
    def get_user_by_ID(self, ID=None):
        # 查找用户
        # Input: ID, int, 用户ID
        # Output: 元组的列表
        if ID:
            CMD = f"""SELECT * FROM {self._tableName} WHERE ID = {ID}"""
        else:
            CMD = f"""SELECT * FROM {self._tableName}"""
        return self._fetch(CMD, "all")
    
    def get_user_by_userName(self, UserName=None):
        # 查找用户
        # Input: UserName, int, 用户名
        # Output: 元组的列表
        if UserName:
            CMD = f"""SELECT * FROM {self._tableName} WHERE UserName = '{UserName}'"""
        else:
            CMD = f"""SELECT * FROM {self._tableName}"""
        return self._fetch(CMD, "all")
    
    def setup(self):
        # 创建一个新表, 仅在测试时使用
        SETUP = f"""CREATE TABLE {self._tableName} (
        ID INTEGER PRIMARY KEY AUTOINCREMENT,
        UserName TEXT NOT NULL, 
        UserType TEXT NOT NULL, 
        TotalToken INTEGER NOT NULL, 
        Day INTEGER NOT NULL,
        Mod TEXT NOT NULL,
        user1 TEXT,
        ai1 TEXT,
        user2 TEXT,
        ai2 TEXT,
        user3 TEXT,
        ai3 TEXT
        )"""
        # 1是最新的聊天记录, 3是最旧的聊天记录
        self._cursor.execute(SETUP)
    
    def _fetch(self, CMD, mod="one"):
        # 执行一条指令并匹配一些数据
        # Input: CMD, str, SQL执行语句
        # Input: mod, str, default="one", 匹配数据数量
        # Output: None/元组
        self._cursor.execute(CMD)
        self._conn.commit()
        if mod == "one":  # 查找一条数据
            data = self._cursor.fetchone()
        elif mod == "all":  # 查找多条数据
            data = self._cursor.fetchall()
        else:
            return None
        return data
    
    def reset(self):
        # 删除表, 仅在测试时使用
        CMD = f"""DROP table {self._tableName}"""
        self._fetch(CMD, "zero")
        self.setup()
    
        
    

if __name__ == "__main__":
    print("Testing: DataBase.py")
    # d = DataBase()
    # print(d.get_user(3))
    # d.reset()