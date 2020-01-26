"""
微信公众平台消息接受与被动回复

"""

from collections import deque
from typing import Callable, Tuple, Any

from . import url

from .. import const
from .. import settings
from ..encrypt import Encrypt

from ...core import wrapper
from ...core.tools import web
from ...core.tools import time
from ...core.tools import encrypt


class Message:
    """
    消息回复管理器:
        register - 注册消息回复函数
        reply - 对给定的包进行回复(包含加/解密流程)
    """

    def __init__(self, encryptor: Encrypt):
        """
        初始化一个消息回复管理器
        以消息类型到用于处理消息函数的映射
        """
        self.__encryptor = encryptor  # 加密处理函数
        self.__registry = {}  # 注册函数处理: str - callable
        self.__exclusion = deque(
            maxlen=settings.Message.ExclusionLength)  # 消息排重队列

    def register(self, typing: str) -> Callable:
        """
        注册一种消息的回复函数
        在微信发来的消息字段 MsgType 中定义的
        字段参数不区分大小写, 调用示例:
            @weixin.reply.register("text")
            def text_reply(**kwargs):
                # 返回一样字符串
                content = kwargs.get("content")
                return content
        """
        def _wrapper(function: Callable[[Any], Tuple[str, dict]]) -> Callable:
            self.__registry.update({typing: function})

        return _wrapper

    @wrapper.timelimit(settings.Message.TimeOut)
    def reply(self, paramaters: list, request: str) -> str:
        """
        返回根据消息调用函数返回回复:
            paramaters: URL参数列表
            request: POST数据字典
        判断加密与进行消息排重
        根据消息类型提取出所有需要的信息
        将信息传入取到的函数进行回复
        """
        encrypted, message = url.verify(self.__encryptor, paramaters, request)

        # 获取五元素
        touser = message.get(const.Message.To)
        fromuser = message.get(const.Message.From)
        _created = message.get(const.Message.CreateTime)
        msgid = message.get(const.Message.Id)
        msgtype = message.get(const.Message.Type)

        # 进行消息排重
        if msgid in self.__exclusion:
            return settings.Message.EmptyReply
        self.__exclusion.append(msgid)

        # 获取需要从包中提取的信息
        needed_keys = const.Message.Types.get(msgtype)
        if needed_keys is None:
            return settings.Message.EmptyReply

        useful = dict()
        for key, value in needed_keys.items():
            useful[value] = message.get(key, '')

        # 获取用于处理的函数
        handler = self.__registry.get(msgtype)
        if handler is None:
            return settings.Message.EmptyReply

        # 获取处理消息
        preduced: dict = handler(**useful)

        reply = {
            const.Message.From: touser,
            const.Message.To: fromuser,
            const.Message.CreateTime: time.now()
        }

        reply.update(preduced)
        reply = web.XMLcreater({const.Message.Root: reply}, encoding=False)

        # 设置回包加密
        if not encrypted:
            return reply

        nonce = encrypt.random(16)
        timestamp = time.nowstr()
        cipher = self.__encryptor.encrypt(reply)
        signature = self.__encryptor.signature(
            cipher, timestamp, nonce)

        reply = {
            const.Encrypt.Message.Content: cipher,
            const.Encrypt.Message.Signature: signature,
            const.Encrypt.Message.TimeStamp: timestamp,
            const.Encrypt.Message.Nonce: nonce
        }
        return web.XMLcreater({const.Message.Root: reply}, encoding=False)
