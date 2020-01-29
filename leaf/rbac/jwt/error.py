"""JWT Token 的相关错误"""

from ...core.error import Error


class InvalidToken(Error):
    """Token 格式错误"""
    code = 12112
    description = "JWT Token 格式错误"


class InvalidHeder(Error):
    """Token 头部格式错误"""
    code = 12111
    description = "JWT Token 头部格式错误/不支持"


class SignatureError(Error):
    """签名计算失败"""
    code = 12113
    description = "JWT Token 的签名计算错误 - 检查secret是否与算法匹配"


class SignatureNotValid(Error):
    """签名验证失败"""
    code = 12114
    description = "JWT Token 签名验证错误"


class TimeExpired(Error):
    """过期错误"""
    code = 12115
    description = "JWT Token 过期"
