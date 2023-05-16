# CatGPT

CatGPT 是部署在广州的腾讯云服务器的项目，功能是登录微信、监听信息、调用 WebAPI、返回微信信息。



## 文件架构

- ./listen.py
  程序主入口。负责监听微信信息并进行处理。
- ./db.py
  定义了对数据库的操作。
- ./chat.py
  负责回复信息。包括调用 API、读取和存储聊天记录。
- ./requests_API.py
  定义了对 API 的调用。API 项目见 ../GPTAPI
- ./lib/itchat/
  itchat 项目的魔改，可以实现 linux 登录电脑版微信。
- ./db/u.db
  数据库。存放用户信息和聊天记录。
- ./db/dbControl.py
  提供给后台维护人员操作数据库的脚本。当需要修改数据库时可以在 Linux 后台执行。



## 如何使用

1. 在 Linux 系统下克隆本项目

   ```bash
   git clone https://github.com/yusijinfs/wxGPT.git
   ```

2. 进入 CatGPT 项目

   ```bash
   cd wxGPT/CatGPT
   ```

3. 开启一个 screen 窗口

   ```bash
   screen
   ```

   如果你未安装 screen，需要先安装

   ```bash
   sudo apt-get install screen
   ```

4. 在 screen 执行 listen.py

   ```bash
   python listen.py
   ```

   或者

   ```bash
   python3 listen.py
   ```

5. 用手机微信扫码登录

6. 退出 screen 窗口

   ```bash
   Ctrl + a d
   ```