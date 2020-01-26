"""
微信公众平台事件类型处理
"""

import logging
from collections import deque
from typing import NoReturn

from . import url

from .. import const
from .. import settings
from ..encrypt import Encrypt

from ...core import events
from ...core import wrapper
from ...core import modules

logger = logging.getLogger("leaf.weixin.reply")
subscribe = events.Event("leaf.weixin.events.subscribe",
                         ((str, int), {}), "用户关注")
unsubscribe = events.Event("leaf.weixin.events.unsubscribe",
                           ((str, int), {}), "用户取消关注")
scan = events.Event("leaf.weixin.events.scan",
                    ((str, int), {"key": str, "ticket": str}), "用户扫描二维码")
location = events.Event("leaf.weixin.events.location",
                        ((str, int), {"latitude": str,
                                      "longitude": str,
                                      "precision": str}),
                        "用户更新地理位置")
click = events.Event("leaf.weixin.events.menu.click",
                     ((str, int), {"key": str}), "用户调取菜单事件")
view = events.Event("leaf.weixin.events.menu.view",
                    ((str, int), {"key": str}), "用户点击菜单进行跳转")
pushed = events.Event("leaf.weixin.events.push.success",
                      ((str, str), {"id": str}), "模板消息推送完成(请自行判断是否成功)")


class Event:
    """
    事件类型处理类:
        handle - 价格事件对应的名称传入, 调用所有绑定事件的函数
    """

    def __init__(self, encryptor: Encrypt):
        """初始化事件处理函数"""
        # 注册事件
        manager: events.Manager = modules.events
        manager.add(subscribe)
        manager.add(unsubscribe)
        manager.add(scan)
        manager.add(location)
        manager.add(click)
        manager.add(view)
        manager.add(pushed)

        # 注册实例
        self.__encryptor = encryptor  # 加解密实例
        self.__exclusion = deque(
            maxlen=settings.Message.ExclusionLength)  # 消息排重队列

    @wrapper.timelimit(settings.Message.TimeOut)
    def handle(self, paramaters: list, request: str) -> NoReturn:
        """
        将事件数据包传入调用事件:
            paramaters: URL参数列表
            request: POST数据字典
        判断加密与进行消息排重
        根据事件类型提取信息
        调用指定的事件
        """
        _encrypted, message = url.verify(self.__encryptor, paramaters, request)

        # 获取用户openid, 事件时间, 事件类型
        user = message.get(const.Message.From)
        created = message.get(const.Message.CreateTime)
        event_type = message.get(const.Event.Type)

        # 进行消息排重
        msgid = user + created
        if msgid in self.__exclusion:
            return
        self.__exclusion.append(msgid)

        # 获取要拉取的事件与参数
        try:
            event_name = const.Event.Events.get(event_type)
            event: events.Event = modules.events.event(event_name)
        except events.EventNotFound as _error:
            logger.error(_error)
            return

        paras = dict()
        for key, value in const.Event.Types.get(event_type):
            paras[value] = message.get(key, '')

        # 拉动事件
        event.notify(user, int(created), **paras)
