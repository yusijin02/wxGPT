import sqlite3

conn = sqlite3.connect('u.db')
c = conn.cursor()
sql = input("Input SQL:")
# 删除 name 为 'John' 的数据
c.execute(sql)

conn.commit()
conn.close()

print("Finish")