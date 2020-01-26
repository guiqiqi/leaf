"""
微信公众平台错误消息相关
"""

from ..core import error


class SignatureError(error.Error):
    """消息体签名错误"""
    code = 12001
    description = "对消息体的签名验证出现错误"


class EncryptError(error.Error):
    """消息体加密错误"""
    code = 12002
    description = "在消息体加密过程中出现错误"


class DecryptError(error.Error):
    """消息体解密错误"""
    code = 12003
    description = "在消息体解密过程中发生错误"


class InvalidMessage(error.Error):
    """消息体非法"""
    code = 12004
    description = "消息体不正确(键缺少/数据类型非法)"
