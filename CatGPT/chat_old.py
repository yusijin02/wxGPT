import db
import request_API
import json

def chat(NickName, wxmsg, temperature=1.0, model="gpt-3.5-turbo", max_tokens=2048):
    history = db.getChatHistory(NickName)
    message = []
    if history is not None:
        for i in range(6):
            if history[i + 2] is not None:
                message.append({
                    'role': 'user' if (i % 2 == 0) else 'assistant',
                    'content': history[i + 2],
                })
    message.append({
        'role': 'user',
        'content': wxmsg,
    })

    flag, res = request_API.post_GPT(messages=message, model=model,
                                temperature=temperature, max_tokens=max_tokens)

    try:
        if flag:
            res_dict = json.loads(res)
            tokens_used = res_dict['res']['usage']['total_tokens']
            text = res_dict['res']['choices'][0]['message']['content']
            if history is None:
                db.update(NickName, None, None, None, None, wxmsg, text)
            else:
                db.update(NickName, history[4], history[5],
                          history[6], history[7], wxmsg, text)
            db.add_tokens(NickName, tokens_used)
            return text
        else:
            text = "[ERROR] 发生了错误, 请稍后重试, 若多次重试均失败, 请联系维护人员.\n\n" + res
            return text
    except Exception as e:
        if history is None:
            text = "[ERROR] 未知错误, 联系维护人员.\n\n" + str(e)
            return text
        else:
            db.update(NickName, None, None, None, None, history[6], history[7])
            history = db.getChatHistory(NickName)
            message = []
            if history is not None:
                for i in range(6):
                    if history[i + 2] is not None:
                        message.append({
                            'role': 'user' if (i % 2 == 0) else 'assistant',
                            'content': history[i + 2],
                        })
            message.append({
                'role': 'user',
                'content': wxmsg,
            })

            flag, res = request_API.post_GPT(messages=message, model=model,
                                             temperature=temperature, max_tokens=max_tokens)
            if flag:
                res_dict = json.loads(res)
                print(res_dict)
                tokens_used = res_dict['res']['usage']['total_tokens']
                text = res_dict['res']['choices'][0]['message']['content']
                if history is None:
                    db.update(NickName, None, None, None, None, wxmsg, text)
                else:
                    db.update(NickName, history[4], history[5],
                              history[6], history[7], wxmsg, text)
                db.add_tokens(NickName, tokens_used)
                return text
            else:
                text = "[ERROR] 发生了错误, 请稍后重试, 若多次重试均失败, 请联系维护人员.\n\n" + res
                return text




def check_user(NickName):
    data = db.get_user(NickName)
    if data is None:
        db.add_user(NickName)
        return None
    else:
        return data[3]



def Admin(cmd_word):
    # 微信命令 操控数据库
    cmd_list = cmd_word.split(" ")
    cmd = cmd_list[0]
    reply = []
    try:
        if cmd in ["h", "H", "help", "Help", "HELP", "帮助"]:
            reply.append(
                "(1)修改用户权限等级\n" +
                "SET <ID> <UserType>\n" +
                "UserType的取值为: ['Baned', 'User', 'VIPUser', 'Admin']"
            )
            reply.append(
                "(2)查询所有用户\n" +
                "USERS\n"
            )
        elif cmd in ["set", "SET", "Set"]:
            ID = cmd_list[1]
            UserType = cmd_list[2]
            if UserType in ["Baned", "User", "VIPUser", "Admin"]:
                db.update_user(ID, UserType)
                reply.append("成功将ID为{}的用户类型设置为{}".format(ID, UserType))
            else:
                reply.append("[ERROR] UserType must be in ['Baned', 'User', 'VIPUser', 'Admin']")
        elif cmd in ["USERS", "Users", "users", "USER", "User", "user"]:
            users_list = db.print_users()
            for user in users_list:
                reply.append("[ID]{}\n\n[NickName]{}\n\n[UserType]{}\n\n[TokensUsage]{}".format(
                    user[0], user[1], user[2], user[3]
                ))
        else:
            reply.append("错误的指令, 请输入 HELP 查看帮助.")
    except Exception as e:
        reply.append("出现异常\n{}".format(str(e)))
    return reply


# if __name__ == "__main__":
#     print(chat("光锥之外", "测试"))