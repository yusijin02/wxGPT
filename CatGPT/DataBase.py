import sqlite3

class DataBase:
    def __init__(self):
        self._path = ".db/user.db"
        self._tableName = "users"
        conn = sqlite3.connect(self._path)
        self.cursor = conn.cursor()
        
    
    def get_history(self, UserName):
        CMD = f"""SELECT (user1, ai1, user2, ai2, user3, ai3) FROM {self._tableName} WHERE UserName = {UserName}"""
        data = self._fetch(CMD)
        return data
    
    def delete_history(self, UserName, num=1):
        if num == 1:  # 删除一条历史记录
            CMD = f"""UPDATE {self._tableName} SET user3 = NULL, ai3 = NULL WHERE UserName = {UserName}"""
        elif num == 2:  # 删除两条历史记录
            CMD = f"""UPDATE {self._tableName} SET user2 = NULL, ai2 = NULL, user3 = NULL, ai3 = NULL 
            WHERE UserName = {UserName}"""
        else:  # 删除所有历史记录
            CMD = f"""UPDATE {self._tableName} SET user1 = NULL, ai1 = NUL, user2 = NULL, ai2 = NULL, user3 = NULL, ai3 = NULL 
            WHERE UserName = {UserName}"""
        self._fetch(CMD, "zero")
    
    def _setup(self):
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
        self.cursor.execute(SETUP)
    
    def _fetch(self, CMD, mod="one"):
        self.cursor.execute(CMD)
        if mod == "one":  # 查找一条数据
            data = self.cursor.fetchone()
        elif mod == "all":  # 查找多条数据
            data = self.cursor.fetchall()
        else:
            return None
        return data
    
    