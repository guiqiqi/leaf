"""微信公众平台设置"""

import os

Interface = "callback"  # 微信公众平台的回调地址
ErrcodesFile = os.path.dirname(os.path.realpath(__file__)) + "/" + "errcodes.json"  # 错误代码存储文件

class User:
    """用户信息相关设置"""
    Language = "zh_CN"  # 获取用户信息的语言版本

class Message:
    """消息相关设置"""
    EmptyReply = "success"  # 回复空消息
    TimeOut = 4.1  # 每个回复消息的超时时间 - 推荐小于 5 秒
    ExclusionLength = 128  # 消息排重队列长度
