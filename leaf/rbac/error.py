"""RBAC 相关的错误定义"""

from ..core import error as _error


class AuthenticationByIdFailed(_error.Error):
    """无法找到Id验证文档"""
    code = 10015
    description = "无法找到该用户的Id验证文档"


class AuthenticationFailed(_error.Error):
    """创建/更新身份验证其余文档时密码验证未通过"""
    code = 10016
    description = "创建/更新身份验证-密码验证失败"


class AuthenticationNotFound(_error.Error):
    """验证文档根据给定的索引未找到"""
    code = 10017
    description = "根据给定的文档索引无法查找到身份验证文档"


class UserNotFound(_error.Error):
    """根据给定信息找不到用户"""
    code = 10018
    description = "根据给定信息找不到用户"


class UserInitialized(_error.Error):
    """用户已经初始化完成"""
    code = 10019
    description = "用户初始化已经完成"


class AccessPointNotFound(_error.Error):
    """访问点无法找到"""
    code = 10020
    description = "根据给定的信息找不到访问点文档"


class GroupNotFound(_error.Error):
    """用户组文档无法找到"""
    code = 10021
    description = "根据给定的信息找不到用户组文档"


class UserIndexValueBound(_error.Error):
    """用户索引信息已经被绑定"""
    code = 10022
    description = "您所给定的用户索引信息已经被绑定"


class UserIndexTypeBound(_error.Error):
    """用户索引类型已经被绑定 - 当前策略不允许多绑定"""
    code = 10023
    description = "您所给定的用户索引类型已经被绑定 - 且当前策略不允许多绑定"


class AuthenticationByIdCanNotDelete(_error.Error):
    """不允许删除根据 Id 创建的认证文档"""
    code = 10024
    description = "不能删除根据 用户Id 创建的认证文档"


class InvalidToken(_error.Error):
    """Token 格式错误"""
    code = 12112
    description = "JWT Token 格式错误"


class InvalidHeder(_error.Error):
    """Token 头部格式错误"""
    code = 12111
    description = "JWT Token 头部格式错误/不支持"


class SignatureError(_error.Error):
    """签名计算失败"""
    code = 12113
    description = "JWT Token 的签名计算错误 - 检查secret是否与算法匹配"


class SignatureNotValid(_error.Error):
    """签名验证失败"""
    code = 12114
    description = "JWT Token 签名验证错误"


class TimeExpired(_error.Error):
    """过期错误"""
    code = 12115
    description = "JWT Token 过期"


class TokenNotFound(_error.Error):
    """在 HTTP Header 信息中没有发现 JWT Token 信息"""
    code = 12116
    description = "在 HTTP Header 信息中没有发现 JWT Token 信息"


class AuthenticationError(_error.Error):
    """身份验证错误"""
    code = 13001
    description = "身份验证错误"


class AuthenticationDisabled(AuthenticationError):
    """该身份验证方式被禁用"""
    code = 13002
    description = "该身份验证方式被禁用"


class InvalidExceptionAccessPonint(_error.Error):
    """前端传入的例外用户组无法识别/用户ID错误"""
    code = 13003
    description = "传入的例外用户组无法被识别/用户ID错误"


class AccessPointNameConflicting(_error.Error):
    """访问点名称冲突"""
    code = 13004
    description = "访问点名称冲突"


class UndefinedUserIndex(_error.Error):
    """未定义的用户索引类型"""
    code = 13005
    description = "未定义的用户索引类型"
