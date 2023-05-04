from lib import itchat
from lib.itchat.content import *
import chat
import time

@itchat.msg_register(TEXT, isFriendChat=True)
def reply(msg):
    text = msg['Text']
    # 在数据库中找到该好友的分级
    friend = itchat.search_friends(userName=msg['FromUserName'])
    NickName = friend['NickName']
    UserType = chat.check_user(NickName)
    # UserType有四个级别："Baned", "User", "VIPUser", "Admin"
    if UserType is None:
        # 该好友第一次出现
        UserType = "User"
        # 通知管理员
        ConsoleAdmin("已添加一位好友进入列表。\nNickName：{}".format(NickName))
        # 修改备注名
    temperature = 1.0
    model = "gpt-3.5-turbo"
    max_tokens = 2048
    if UserType in ["VIPUser", "Admin"]:
        # 可以使用开发者模式
        if text[0:2] == ":\n":
            msg_list = text.split("\nEND;\n")
            if len(msg_list) == 2 and msg_list[1]:
                text = msg_list[1]
                cmd_list = msg_list[0].split("\n")
                for cmd in cmd_list:
                    cmd_word_list = cmd.split(" ")
                    if len(cmd_word_list) == 3:
                        if cmd_word_list[0] == "SET":
                            if cmd_word_list[1] == "temperature":
                                temperature = float(cmd_word_list[2].replace(";", ""))
                            if cmd_word_list[1] == "model":
                                model = cmd_word_list[2].replace(";", "")
                            if cmd_word_list[1] == "max_token":
                                max_tokens = int(cmd_word_list[2].replace(";", ""))
    reply = "[错误]"
    try:
        reply = chat.chat(NickName, text, temperature=temperature, model=model, max_tokens=max_tokens)
    except Exception as e:
        reply = reply + str(e)
    friend.send(reply)



def ConsoleAdmin(info):
    group = itchat.search_chatrooms(name='AdminGroup')[0]
    group.send(info)




@itchat.msg_register(TEXT, isGroupChat=True)
def group_reply(msg):
    if msg.isAt:
        reply = chat.chat(msg['FromUserName'], msg.text)
        itchat.send(reply, msg['FromUserName'])
    else:
        if itchat.search_chatrooms(name='AdminGroup')[0]['UserName'] == msg['FromUserName']:
            # 是管理员群
            reply_list = chat.Admin(msg.text)
            for reply in reply_list:
                itchat.send(reply, msg['FromUserName'])
                time.sleep(1)












def debug():
    pass


itchat.auto_login(enableCmdQR=-2)
itchat.run()



