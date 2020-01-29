"""JWT Token相关设置"""

from ...core.tools import encrypt


class Signature:
    """签名相关设置"""
    Algorithm = ("HS256", encrypt.HMAC_SHA256)  # 默认签名算法
    ValidPeriod = 3600 # 默认 Token 有效期


class Payload:
    """自定义载荷部分设置"""
    Permission = "permission"  # 签发时的用户权限
