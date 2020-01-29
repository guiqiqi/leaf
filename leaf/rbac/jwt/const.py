"""JWT Token常量相关设置"""


class Header:
    """头部相关设置"""
    Type = "typ"  # 类型
    Algorithm = "alg"  # 加密算法

    @staticmethod
    def make(algorithm: str) -> dict:
        """生成头部"""
        return {
            Header.Type: "JWT",
            Header.Algorithm: algorithm
        }


class Payload:
    """载荷相关常量"""
    Issuer = "iss"  # 签发者
    Expiration = "exp"  # 过期时间
    IssuedAt = "iat"  # 签发时间
    Audience = "aud"  # 颁发对象
