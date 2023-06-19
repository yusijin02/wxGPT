import requests
import time
import hashlib


def get_s(k, t):
    _s = k + t
    hash_object = hashlib.sha256()
    hash_object.update(_s.encode())
    return hash_object.hexdigest()

def log(info):
    print(info)

def get_GPT(
                messages="[{'role': 'user', 'content': '请介绍你自己'}]",  # 对话内容
                model="gpt-3.5-turbo",  # 使用的模型
                max_tokens=2048,  # 最大回复token
                timeout=120,  # 最长等待时间
                retry=3,  # 重试次数
                proxy=None,  # 代理
            ):
    k = "GR0J69bhDtn8g1c5LQXaSYKjxpvMWPykwIsZNUuB7VefFEmzH4dAoOTCq2lVi3"
    t = str(time.time())
    s = get_s(k, t)
    u = "http://103.143.248.145:1314/api/ChatGPT/?t={}&k={}&s={}&model={}&messages={}&max_tokens={}".format(
        t, k, s, model, messages, max_tokens
    )
    for _ in range(retry):
        try:
            res = requests.get(u, proxies=proxy, timeout=timeout)
            return True, res.text
        except Exception as e:
            log("[ERROR]" + str(e))
    return False, ""

def post_GPT(
                messages,  # 对话内容
                model="gpt-3.5-turbo",  # 使用的模型
                max_tokens=2048,  # 最大回复token
                timeout=120,  # 最长等待时间
                retry=3,  # 重试次数
                proxy=None,  # 代理
                temperature=1.0
            ):
    k = "GR0J69bhDtn8g1c5LQXaSYKjxpvMWPykwIsZNUuB7VefFEmzH4dAoOTCq2lVi3"
    t = time.time()
    s = get_s(k, str(t))
    data = {
        'k': k,
        't': t,
        's': s,
        'messages': messages,
        'model': model,
        'max_tokens': max_tokens,
        'temperature': temperature,
    }
    u = "http://103.143.248.145:1314/api/ChatGPT_post/"
    for _ in range(retry):
        try:
            res = requests.post(u, json=data, proxies=proxy, timeout=timeout)
            return True, res.text
        except Exception as e:
            log("[ERROR]" + str(e))
    return False, str(e)

def test():
    flag, res = get_GPT()
    print(flag)
    print(res)
    print("=========GET=========")
    flag, res = get_GPT(messages="[{'role': 'user', 'content': 'What is your name?'}]", max_tokens=256)
    print(flag)
    print(res)

    print("==========POST========")
    flag, res = post_GPT(messages=[{'role': 'user', 'content': 'What\'s your name?'}], max_tokens=256)
    print(flag)
    print(res)


if __name__ == "__main__":
    print("test start, wait.")
    test()
