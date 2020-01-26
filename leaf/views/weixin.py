"""微信公众平台回调函数支持"""

from flask import request
from flask import Blueprint

from ..core import modules

from ..weixin import const
from ..weixin import settings
from ..weixin.reply import Event
from ..weixin.reply import Message

weixin = Blueprint("weixin", __name__)


@weixin.route("/" + settings.Interface, methods=["GET", "POST"])
def message_and_event_preducer():
    """处理微信发来的消息和事件"""

    # 微信消息加密与签名实例引用
    message_handler: Message = modules.weixin.message
    event_handler: Event = modules.weixin.event

    # 获取 url 参数和 post 参数
    message: str = request.data.decode()
    paramaters: dict = request.args.to_dict()

    # 是否为回显消息
    if const.Encrypt.URL.Key.Echo in paramaters.keys():
        return paramaters.get(const.Encrypt.URL.Key.Echo)

    # 判断是消息类型还是事件类型
    try:
        if const.Message.Message in message:
            reply = message_handler.reply(paramaters, message)
            return reply

        if const.Message.Event in message:
            event_handler.handle(message)
            return settings.Message.EmptyReply

    # 当超时错误之后返回自定义空消息
    except TimeoutError as _error:
        return settings.Message.EmptyReply

    return settings.Message.EmptyReply
