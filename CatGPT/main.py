from lib import itchat
from lib.itchat.content import *
import threading
from ListeningWindows import ListeningMessages

@itchat.msg_register(TEXT, isFriendChat=True)  # 监听好友信息
def replyFriend(msg):
    text = msg['Text']
    UserName = msg['FromUserName']
    friend = itchat.search_friends(userName=UserName)
    if text[0] == "#":
        # 指令
        pass
    else:
        windows = ListeningMessages(UserName, text)
        windows.run()
        friend.send(windows.reply)
