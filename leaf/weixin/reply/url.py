"""URL 参数验证器"""

from typing import Tuple

from .. import const
from .. import error

from ..encrypt import Encrypt
from ...core.tools import web


class URLParamater:
    """URL 参数处理器"""

    @staticmethod
    def nonce(paramaters: dict) -> str:
        """返回 URL 中的 Nonce"""
        return paramaters.get(const.Encrypt.URL.Key.Nonce, '')

    @staticmethod
    def timestamp(paramaters: dict) -> str:
        """返回时间戳参数"""
        return paramaters.get(const.Encrypt.URL.Key.TimeStamp, '')

    @staticmethod
    def siganture(paramaters: dict) -> str:
        """返回消息体签名"""
        return paramaters.get(const.Encrypt.URL.Key.Signature, '')

    @staticmethod
    def encrypted(paramaters: dict) -> bool:
        """判断数据包是否是加密的"""
        encrypt_type = paramaters.get(const.Encrypt.URL.Key.Encrypted)
        if encrypt_type == const.Encrypt.URL.Value.Encrypted:
            return True
        return False


def verify(encryptor: Encrypt, paramaters: list, request: str) -> Tuple[bool, dict]:
    """
    验证加密是否正确
    尝试解密后将xml转为字典输出
    返回是否加密的 bool 值与解包后的字典
    """
    request = web.XMLparser(request)

    # 获取URL中的参数
    encrypted = URLParamater.encrypted(paramaters)
    signature = URLParamater.siganture(paramaters)
    nonce = URLParamater.nonce(paramaters)
    timestamp = URLParamater.timestamp(paramaters)

    # 判断是否加密
    if not encrypted:
        return False, request

    # 验证加密是否正确
    encrypted_msg: str = request.get(const.Encrypt.Message.Content)
    expectation = encryptor.signature(
        encrypted_msg, timestamp, nonce)
    if expectation != signature:
        raise error.SignatureError(expectation + ' - ' + signature)

    # 解密数据包
    try:
        message = encryptor.decrypt(encrypted_msg.encode())
    except ValueError as _error:
        raise error.DecryptError(_error)

    message = web.XMLparser(message)
    return True, message
