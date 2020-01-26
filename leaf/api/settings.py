"""API 接口的设置文件"""


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
