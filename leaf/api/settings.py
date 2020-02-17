"""API 接口的设置文件"""

from typing import Optional
from flask import abort
from ..core import error


class Authorization:
    """权限验证中的设置"""

    ExecuteAPMissing = True  # 在未找到接入点信息时是否允许

    @staticmethod
    def UnAuthorized(_reason: error.Error):
        """
        验证失败时的返回值:
            _reason: 原因-错误类型
        """
        return abort(403)

    @staticmethod
    def NotPermitted(_diff: int, _strict: Optional[bool] = False):
        """
        权限不足时的返回值:
            _diff: 所需权限与拥有权限的差值
            _strict: 是否指定需要某一级别权限值
        """
        return abort(403)


class Response:
    """响应中的设置"""
    Code = "code"  # 错误代码键
    Description = "description"  # 错误解释键
    Message = "message"  # 错误消息键

    class Codes:
        """响应代码设置"""
        Success = 0  # 未发生错误的成功代码
        Unknown = -1  # 未知错误代码

    class Messages:
        """响应消息设置"""
        Success = "success"  # 未发生错误时的成功消息
        Unknown = "undefined"  # 未知错误消息

    class Descriptions:
        """响应解释设置"""
        Success = "成功"  # 成功时的解释
        Unknown = "发生未知错误"  # 未知错误解释
