import sqlite3
from datetime import date


def setup():
    # 只用于设定
    conn = sqlite3.connect('./db/u.db')
    cursor = conn.cursor()
    cursor.execute("""CREATE TABLE chatHistory
                    (id INTEGER PRIMARY KEY AUTOINCREMENT, userName TEXT NOT NULL, 
                    histroy_user_1 TEXT, history_assistant_1 TEXT,
                    histroy_user_2 TEXT, history_assistant_2 TEXT,
                    histroy_user_3 TEXT, history_assistant_3 TEXT)""")
    cursor.execute("""CREATE TABLE users (id INTEGER PRIMARY KEY AUTOINCREMENT,
                      UserName TEXT NOT NULL, UserType TEXT NOT NULL, TotalToken INTEGER NOT NULL, 
                      Day INTEGER NOT NULL)""")
    conn.commit()
    conn.close()


def reset():
    # 删除全表
    conn = sqlite3.connect('./db/u.db')
    cursor = conn.cursor()
    cursor.execute("""DROP TABLE chatHistory;""")
    cursor.execute("""DROP TABLE users;""")
    setup()


def update(userName, um1=None, am1=None, um2=None, am2=None, um3=None, am3=None):
    conn = sqlite3.connect('./db/u.db')
    cursor = conn.cursor()
    # 获取该用户的历史聊天记录
    cursor.execute("SELECT * FROM chatHistory WHERE userName = ?", (userName, ))
    data = cursor.fetchone()
    if data is None:
        # 没有该用户的聊天记录
        cursor.execute("""INSERT INTO chatHistory (userName, 
                                             histroy_user_1, history_assistant_1, 
                                             histroy_user_2, history_assistant_2,
                                             histroy_user_3, history_assistant_3) 
                                VALUES (?, ?, ?, ?, ?, ?, ?)""",
                       (userName, um1, am1, um2, am2, um3, am3))
    else:
        # 有该用户的历史聊天记录
        cursor.execute("""UPDATE chatHistory SET histroy_user_1 = ?, history_assistant_1 = ?, 
                                           histroy_user_2 = ?, history_assistant_2 = ?,
                                           histroy_user_3 = ?, history_assistant_3 = ? WHERE userName = ?""",
                       (um1, am1, um2, am2, um3, am3, userName))
    conn.commit()
    conn.close()

def getChatHistory(userName):
    conn = sqlite3.connect('./db/u.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM chatHistory WHERE userName = ?", (userName,))
    data = cursor.fetchone()
    conn.commit()
    conn.close()
    return data


def add_user(UserName, UserType='User', TotalToken=0):
    today = date.today().day
    conn = sqlite3.connect('./db/u.db')
    cursor = conn.cursor()
    cursor.execute("""INSERT INTO users (UserName, UserType, TotalToken, Day)
                      VALUES (?, ?, ?, ?)""",
                   (UserName, UserType, TotalToken, today))
    conn.commit()
    conn.close()


def update_user(ID, UserType):
    conn = sqlite3.connect('./db/u.db')
    cursor = conn.cursor()
    cursor.execute("""UPDATE users SET UserType = ? WHERE id= ?""", (UserType, ID))
    conn.commit()
    conn.close()
    
def update_date(ID, Day):
    conn = sqlite3.connect('./db/u.db')
    cursor = conn.cursor()
    cursor.execute("""UPDATE users SET Day = ? WHERE id= ?""", (Day, ID))
    conn.commit()
    conn.close()

def count_userType(UserType):
    conn = sqlite3.connect('./db/u.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT COUNT(*) FROM users WHERE UserType = ?""", (UserType, ))
    result = cursor.fetchone()[0]
    conn.commit()
    conn.close()
    return result

def print_users():
    conn = sqlite3.connect('./db/u.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM users""")
    result = cursor.fetchall()
    conn.commit()
    conn.close()
    return result

def add_tokens(UserName, tokens):
    conn = sqlite3.connect('./db/u.db')
    cursor = conn.cursor()
    cursor.execute(f"""UPDATE users SET TotalToken = TotalToken + {tokens} WHERE UserName = ?""", (UserName, ))
    conn.commit()
    conn.close()

def get_user(UserName):
    conn = sqlite3.connect('./db/u.db')
    cursor = conn.cursor()
    cursor.execute("""SELECT * FROM users WHERE UserName = ?""", (UserName, ))
    data = cursor.fetchone()
    conn.commit()
    conn.close()
    return data

def test():
    update("test_1", "聊天记录1", "聊天记录2")
    update("test_2", "聊天记录1", "聊天记录2", "聊天记录3", "聊天记录4", "聊天记录5", "聊天记录6")
    print(getChatHistory("test_1"))
    print(getChatHistory("test_2"))
    print(getChatHistory("test_3"))
    add_user('2', 'test')
    add_user('3', 'test', 10)
    print(print_users())
    print(count_userType('test'))
    update_user('3', 'test2')
    add_tokens('3', 100)
    print(print_users())





if __name__ == "__main__":
    reset()
    test()
    reset()
