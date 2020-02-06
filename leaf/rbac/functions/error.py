"""RABC 相关错误"""

from ...core import error


class AuthenticationByIdFailed(error.Error):
    """无法找到Id验证文档"""
    code = 10015
    description = "无法找到该用户的Id验证文档"


class AuthenticationFailed(error.Error):
    """创建/更新身份验证其余文档时密码验证未通过"""
    code = 10016
    description = "创建/更新身份验证-密码验证失败"


class AuthenticationNotFound(error.Error):
    """验证文档根据给定的索引未找到"""
    code = 10017
    description = "根据给定的文档索引无法查找到身份验证文档"


class UserNotFound(error.Error):
    """根据给定信息找不到用户"""
    code = 10018
    description = "根据给定信息找不到用户"


class UserInitialized(error.Error):
    """用户已经初始化完成"""
    code = 10019
    description = "用户初始化已经完成"


class AccessPointNotFound(error.Error):
    """访问点无法找到"""
    code = 10020
    description = "根据给定的信息找不到访问点文档"


class GroupNotFound(error.Error):
    """用户组文档无法找到"""
    code = 10021
    description = "根据给定的信息找不到用户组文档"


class UserIndexValueBound(error.Error):
    """用户索引信息已经被绑定"""
    code = 10022
    description = "您所给定的用户索引信息已经被绑定"


class UserIndexTypeBound(error.Error):
    """用户索引类型已经被绑定 - 当前策略不允许多绑定"""
    code = 10023
    description = "您所给定的用户索引类型已经被绑定 - 且当前策略不允许多绑定"
