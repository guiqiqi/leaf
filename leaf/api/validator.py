"""API 函数工具库"""

from typing import List

import bson
from flask import g as _g
from flask import request as _request

from . import error
from .. import rbac


def objectid(obj: str) -> bson.ObjectId:
    """
    验证是否为合法的 ObjectId:
        当传入的字符串为合法的 ObjectId 时返回 ObjectId 对象
        否则掷出 error.InvalidObjectId 错误
    """
    try:
        return bson.ObjectId(obj)
    except bson.errors.InvalidId as _error:
        raise error.InvalidObjectId(obj)


def operator(modified: str) -> bson.ObjectId:
    """
    检查当前的操作者是否为指定对象(被修改对象):
        当检查不通过时则掷出 rbac.error.AuthenticationError
        当检查通过时候返回操作者的 userid: bson.ObjectId 对象
    """
    try:
        checkuser: bool = _g.checkuser
        _operator: str = _g.operator
    except AttributeError as _error:
        raise rbac.error.AuthenticationError(modified)

    # 当检查到操作者和被操作者不是同一用户时
    if checkuser and str(modified) != _operator:
        raise rbac.error.AuthenticationError(operator)
    return objectid(modified)


def jwttoken() -> dict:
    """
    验证传入的 JWT Token 是否正确并返回 payload, 可能的错误:
        rbac.jwt.error.InvalidToken - Token 解析失败
        rbac.jwt.error.TokenNotFound - 未找到 Token
        rbac.jwt.error.InvalidHeader - 非法的头部信息
        rbac.jwt.error.TimeExired - Token 已经过期
        rbac.jwt.error.SignatureNotValid - 签名信息验证失败
    """
    # 获取 Bearer-Token
    authorization: str = _request.headers.get("Authorization")

    # 通过 Authorization 头获取 Token
    token: str = str()
    if not authorization:
        raise rbac.error.TokenNotFound()
    token = authorization.replace("Bearer", '', 1)

    # 验证 JWT Token 信息
    verification = rbac.jwt.Verify(token)
    verification.header()
    payload = verification.payload()

    # 通过 payload 获取用户盐并判断 Token 是否正确
    userid = payload.get(rbac.jwt.const.Payload.Audience)
    salt = rbac.functions.auth.Retrieve.saltbyindex(str(userid))
    verification.signature(salt)

    return payload


def permission(pointname: str, payload: dict) -> int:
    """
    验证 JWT Token 的权限是否足够访问对应接入点:
        pointname: 接入点名称
        payload: JWT Token 的 Payload 部分

    返回的数值 diff: int 表示所需权限差:
        diff == 0 - 表示权限验证符合
        diff < 0 - 表示所需要权限不足(返回的差表示差多少)
        diff > 0 - 表示所需要权限足够但该访问点要求用户组对应

    可能返回的错误:
        rbac.functions.error.AccessPointNotFound - 未找到对应的接入点信息
        bson.errors.InvalidId - 非法的 UserId 信息
    """
    # 获取权限点所需要的权限
    permitted: List[int] = payload.get(rbac.jwt.settings.Payload.Permission)
    accesspoint = rbac.functions.accesspoint.Retrieve.byname(pointname)
    if not accesspoint:
        raise rbac.error.AccessPointNotFound(pointname)
    userid = objectid(payload.get(rbac.jwt.const.Payload.Audience))

    # 验证是否是特权用户
    if userid in accesspoint.exception:
        return 0

    # 检查是否需要指定用户组
    if accesspoint.strict:
        if not accesspoint.required in permitted:
            return max(permitted) - accesspoint.required
        return 0

    # 检查权限是否足够
    if accesspoint.required > max(permitted):
        return max(permitted) - accesspoint.required
    return 0
