from wxpy import *

bot = Bot()

# 找到一个好友
friend = bot.friends().search('好友昵称')[0]

# 自动回复好友信息
@bot.register(friend)
def reply_my_friend(msg):
    print(msg)
    return '你好，我收到了你的消息：{}'.format(msg.text)

# 让程序保持运行
embed()
