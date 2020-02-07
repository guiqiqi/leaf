"""JWT Token 类"""

from typing import Tuple, Optional, Callable, NoReturn, Dict

from ...core.tools import web
from ...core.tools import time
from ...core.tools import encrypt

from . import const
from . import settings


class Token:
    """Token 计算与生成器"""

    def __init__(self, secret: str):
        """
        Token 类构造函数:
            parts: 部分令牌
            secret: 签名密钥
            algorithm: 在设置头部时指定算法
        """
        self.__parts = list()
        self.__secret: str = secret
        self.__algorithm: Callable[[bytes, bytes], str] = None

    def header(self, algorithm: Optional[Tuple[str, Callable]]
               = settings.Signature.Algorithm) -> NoReturn:
        """计算头部字符串"""
        header = const.Header.make(algorithm[0])
        self.__algorithm = algorithm[1]
        text = web.JSONcreater(header)
        self.__parts.append(encrypt.base64encode_url(text.encode()).decode())

    def payload(self, issuer: str, audience: str,
                period: int = settings.Signature.ValidPeriod,
                other: Optional[Dict[str, str]] = None) -> NoReturn:
        """计算载荷部分的值"""
        now = time.now()
        payload = {
            const.Payload.Issuer: issuer,
            const.Payload.Audience: audience,
            const.Payload.IssuedAt: now,
            const.Payload.Expiration: now + period
        }
        if not other is None:
            payload.update(other)
        text = web.JSONcreater(payload)
        self.__parts.append(encrypt.base64encode_url(text.encode()).decode())

    def issue(self) -> str:
        """签名之后返回可用的Token"""
        content = '.'.join(self.__parts)
        signature = self.__algorithm(content.encode(), self.__secret.encode())
        return content + '.' + encrypt.base64encode_url(signature).decode()
