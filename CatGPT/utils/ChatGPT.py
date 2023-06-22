import hashlib
import time
import json
import requests

class ChatGPT:
    def __init__(self):
        self._message = list()
        
        self._k = "GR0J69bhDtn8g1c5LQXaSYKjxpvMWPykwIsZNUuB7VefFEmzH4dAoOTCq2lVi3"
        
        self.set_model()
        self.set_max_tokens()
        self.set_timeout()
        self.set_retry()
        self.set_temperature()
        
        self._proxy = None
        self.log = print
        self._json = None
        
        self.code = 400
        self.state = "Not Recived"
        self._dic_res = None
        self.id = None
        self.object = None
        self.created = None
        self.model = None  # ChatGPT回复的json数据的字段
        self.usage = None
        self.total_tokens = None
        self.reply = None
        
    def run(self):
        if self._get_reply():
            self._json2text()
            return True if self.reply else False
        return False
    
    
    def _set_msg(self, role, content):
        self._message.append({"role": role, "content": content})
        
    def _get_s(self):
        """计算加密参数"""
        self._s = self._k + str(self._t)
        hash_object = hashlib.sha256()
        hash_object.update(self._s.encode())
        return hash_object.hexdigest()
    
    def set_model(self, model="gpt-3.5-turbo"):
        """使用的模型"""
        self._model = model
        
    def set_max_tokens(self, max_tokens=2048):
        """最长回复token"""
        self._max_tokens = max_tokens
    
    def set_timeout(self, timeout=180):
        """最长等待时间"""
        self._timeout = timeout
    
    def set_retry(self, retry=3):
        """重试次数"""
        self._retry = retry
    
    def set_temperature(self, temperature=1.0):
        """温度超参数"""
        self._temperature = temperature
    
    def set_proxy(self, proxy):
        self._proxy = proxy
    
    def _get_reply(self):
        self._t = time.time()
        self._s = self._get_s()
        data = {
            'k': self._k,
            't': self._t,
            's': self._s,
            'messages': self._message,
            'model': self._model,
            'max_tokens': self._max_tokens,
            'temperature': self._temperature,
        }
        u = "http://103.143.248.145:1314/api/ChatGPT_post/"
        for _ in range(self._retry):
            try:
                self._json = requests.post(u, json=data, proxies=self._proxy, timeout=self._timeout).text
                return True
            except Exception as e:
                self.log(str(e))
        return False
    
    def add_system_prompt(self, msg):
        self._set_msg("system", msg)
        
    def add_examples(self, qst, ans):
        self._set_msg("user", qst)
        self._set_msg("assistant", ans)
        
    def add_question(self, qst):
        self._set_msg("user", qst)
        
    def get_message(self):
        return self._message
    
    def _json2text(self):
        _dic = json.loads(self._json)
        try:
            self.code = int(_dic["code"])
            self.state = _dic["state"]
            self._dic_res = _dic["res"]
            self.id = self._dic_res["id"]
            self.object = self._dic_res["object"]
            self.created = self._dic_res["created"]
            self.model = self._dic_res["model"]
            self.usage = self._dic_res["usage"]
            self.total_tokens = self.usage["total_tokens"]
            self.reply = self._dic_res["choices"][0]["message"]["content"]
        except Exception as e:
            self.log(str(e))
            
        
        
if __name__ == '__main__':
    print("Testing: utils.ChatGPT.py")
    c = ChatGPT()
    c.add_question("Please introduce yourself.")
    print(c.run())
    print(c.reply)