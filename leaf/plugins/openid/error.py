"""
OpenID 获取错误定义
"""

from ...core.error import Error


class PatchError(Error):
    """获取openid错误"""
    code = 40029
    description = "获取openid错误"
