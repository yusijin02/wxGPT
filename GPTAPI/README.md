# GPTAPI

GPTAPI 是部署在洛杉矶的亿速云服务器的项目，功能是将用户提交的信息 (json 数据) 放入 OpenAI 的 API 中，并把 OpenAI 返回的结果 (json 数据) 返回给用户。



## 文件架构

- ./Key.py
  存放本项目的用户 Key 和你的 OpenAI Key
- ./start.sh
  一键部署项目的脚本
- 其余的文件均为 Django WebAPI 框架



## 如何使用

1. 在 Linux 系统下克隆本项目

   ```bash
   git clone https://github.com/yusijinfs/wxGPT.git
   ```

2. 将 ./Key.py 文件进行配置：

   ```python
   Key = [
       "用户 KEY 0",
       "用户 KEY 1",
   ]
   
   Api_Key = "你的 OpenAI API KEY"
   ```

   - `Key` 放入你的用户 Key。只有带有这些 Key 的用户才有资格使用你的 WebAPI
   - `Api_Key` 放入你的 OpenAI 官方的 API Key。

3. 执行 ./start.sh 一键开启

   ```bash
   bash start.sh
   ```

   