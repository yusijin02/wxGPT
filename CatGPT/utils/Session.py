import threading
from ListeningWindows import ListeningMessages

def replyFriend(text, userName, friend):
    
    if text[0] == "#":
        # 指令
        pass
    else:
        windows = ListeningMessages(userName, text)
        windows.run()
        friend.send(windows.reply)