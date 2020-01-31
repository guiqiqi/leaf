"""JWT Token 验证模块"""

from typing import NoReturn, Callable, Optional, Tuple

from ...core.tools import web
from ...core.tools import time
from ...core.tools import encrypt

from . import error
from . import const
from . import settings


class Verify:
    """JWT Token 验证类"""

    def __init__(self, token: str):
        """
        JWT Token验证类:
            分割并检查Token格式是否正确
            还原被encode的信息
            algorithm - 使用的加密算法
            content - 无签名部分的token
        """
        try:
            header, payload, signature = token.split('.')
        except ValueError as _error:
            raise error.InvalidToken(token)

        self.__algorithm: Callable[[bytes, bytes], str] = None
        self.__header: str = encrypt.base64decode_url(header.encode()).decode()
        self.__payload: str = encrypt.base64decode_url(payload.encode()).decode()
        self.__content: str = header + '.' + payload
        self.__signature: bytes = encrypt.base64decode_url(signature.encode())

    def header(self, algorithm: Optional[Tuple[str, Callable]]
               = settings.Signature.Algorithm) -> dict:
        """验证头部信息是否正确"""
        header = web.JSONparser(self.__header)
        target = const.Header.make(algorithm[0])
        self.__algorithm = algorithm[1]

        if target != header:
            raise error.InvalidHeder(str(header))

        return header

    def payload(self) -> dict:
        """验证是否过期"""
        payload = web.JSONparser(self.__payload)
        now = time.now()
        expired = payload.get(const.Payload.Expiration)
        if now > expired:
            raise error.TimeExpired("过期在: " + time.timestr(expired))

        return payload

    def signature(self, secret: str) -> NoReturn:
        """验证签名是否正确"""
        target = self.__algorithm(self.__content.encode(), secret.encode())
        if target != self.__signature:
            raise error.SignatureNotValid(self.__signature)
