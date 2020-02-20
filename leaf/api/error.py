"""API 错误定义"""

from ..core import error


class InvalidObjectId(error.Error):
    """非法的 ObjectId"""
    code = 10010
    description = "非法的 ObjectId 字符串"
