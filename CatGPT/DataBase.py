import sqlite3
from datetime import date

class DataBase:
    def __init__(self):
        self._path = "./db/user.db"

        self._tableName = "users"
        self._conn = sqlite3.connect(self._path)
        self._cursor = self._conn.cursor()
        
    def get_history(self, UserName):
        CMD = f"""SELECT user1, ai1, user2, ai2, user3, ai3 FROM {self._tableName} WHERE UserName = '{UserName}'"""
        data = self._fetch(CMD)
        return data
    
    def delete_history(self, UserName, num=1):
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
        _hty = self.get_history(UserName)
        if not _hty:  # 如果没有历史记录, 容易产生bug
            return
        user1, ai1, user2, ai2 = _hty[0], _hty[1], _hty[2], _hty[3]
        CMD = f"""UPDATE {self._tableName} SET user1 = '{user}', ai1 = '{ai}', 
        user2 = '{user1}', ai2 = '{ai1}', user3 = '{user2}', ai3 = '{ai2}' WHERE UserName = '{UserName}'"""
        self._fetch(CMD, "zero")    
        
    def add_user(self, UserName):
        day = date.today().day
        UserType = "User"
        TotalToken = 0
        Mod = "Chat"
        CMD = f"""INSERT INTO {self._tableName} (UserName, UserType, TotalToken, Day, Mod, user1, ai1, user2, ai2, user3, ai3) VALUES 
        ('{UserName}', '{UserType}', {TotalToken}, {day}, '{Mod}', NULL, NULL, NULL, NULL, NULL, NULL)"""
        self._fetch(CMD, "zero")
    
    def setup(self):
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
        self._cursor.execute(CMD)
        self._conn.commit()
        if mod == "one":  # 查找一条数据
            data = self._cursor.fetchone()
        elif mod == "all":  # 查找多条数据
            data = self._cursor.fetchall()
        else:
            return None
        return data
    

if __name__ == "__main__":
    print("Testing: DataBase.py")
    d = DataBase()
    # d.add_user("2")
    d.update_history("2", "user said", "ai said")
    print(d.get_history("2"))