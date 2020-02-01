"""RABC 相关错误"""

from ...core import error


class AuthenticationByIdFailed(error.Error):
    """创建其余身份验证文档时无法找到Id验证文档"""
    code = 10015
    description = "无法找到该用户的Id验证文档"


class AuthenticationFailed(error.Error):
    """创建身份验证其余文档时密码验证未通过"""
    code = 10016
    description = "创建身份验证-密码验证失败"
