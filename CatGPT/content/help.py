HELP = """##########
指令(包括井号与它后面的空格, 不包括分号); 功能
##########
# help; 帮助
# DefaultMod; 普通模式(CatGPT v1)
# ChatMod; 聊天模式
# PromptMod; 开发者模式
# PaperMod; 写论文模式
# PPTMod; 辅助PPT模式
# TransMod; 翻译模式
# bug; 快捷差错报告
# check; 查看月结算日

使用 help 指令名, 可以更详细地获得介绍, 例如:
# help PromptMod; 查看辅助PPT模式的介绍"""

PromptMod = """##########
开发者模式的介绍
##########
在系统提示模式下, 你可以自由地设置传递的信息. 若您不是专业人士, 请谨慎操作.
[注意事项]
1. 请使用标准的JSON格式作为输入. 错误的输入格式将引起报错.
2. 输出的结果将使用JSON格式.
3. AI不会记忆任何的聊天记录.
[输入格式]
[{"role": "system", "content": "你的提示语"},
 {"role": "user", "content": "你的训练样本(输入)"},
 {"role": "assistant", "content": "你的训练样本(输出)"}]
"""