"""API 函数的包装器"""

import sys
import json
import types
import logging
import datetime
import ipaddress
import traceback
from typing import Callable, Type, Dict,\
    NoReturn, Optional, Iterable, Any

import bson
import mongoengine
from flask import g as _g
from flask import abort as _abort
from flask import request as _request
from flask import Response as _Response
from werkzeug.exceptions import HTTPException

from . import settings
from . import validator
from .. import rbac
from ..core import error


logger = logging.getLogger("leaf.api")


class __TypeConverter:
    """类型转换注册器"""

    def __init__(self):
        """初始化一个转换注册表"""
        self.__default = str  # 默认转换器
        self.__converters: Dict[Type, Callable[[Type], object]] = dict()

    def set_default(self, default: Callable[[Type], object]) -> NoReturn:
        """设置默认转换器"""
        self.__default = default

    def register(self, typing: Type, _converter: Callable[[Type], object]):
        """注册一个转换器"""
        self.__converters[typing] = _converter

    def convert(self, obj: object, default: Optional[bool] = False) -> object:
        """
        按照注册的顺序进行类型转换
        当传入 default 参数为 true 时调用设置的默认转换器
        """

        for _type, _converter in self.__converters.items():
            if isinstance(obj, _type):
                return _converter(obj)

        if not default:
            raise KeyError("can not find converter for type %s" %
                           str(type(obj)))

        return self.__default(obj)


# 生成类型转换器实例
converter = __TypeConverter()
converter.set_default(str)
converter.register(bson.ObjectId, str)
converter.register(datetime.datetime, lambda obj: obj.isoformat())
converter.register(datetime.time, lambda obj: obj.isoformat)
converter.register(Exception, str)
converter.register(mongoengine.QuerySet, list)
converter.register(mongoengine.Document, lambda obj: obj.to_json())
converter.register(mongoengine.EmbeddedDocument, lambda obj: obj.to_json())


class Encoder(json.JSONEncoder):
    """
    重写 json.JSONEncoder.default 函数
    在其中加入自定义的类型转换
    """

    # pylint: disable=method-hidden
    # pylint: disable=arguments-differ
    def default(self, obj):
        """设置类型转换"""
        try:
            return converter.convert(obj)
        except KeyError as _error:
            pass

        return json.JSONEncoder.default(self, obj)

    types.MethodType(default, json.JSONEncoder)


def jsonify(*args, **kwargs):
    """返回自定义格式的 JSON 数据包"""
    return _Response(
        json.dumps(dict(*args, **kwargs), cls=Encoder),
        mimetype="application/json"
    )


def iplimit(allowed: Iterable[str]) -> Callable:
    """
    一个 API 接口访问限制 (基于 IP 地址)
    如果不在允许的 IP 列表范围内则返回 403:
        @api.iplimit("127.0.0.1") -> only localhost
        @api.iplimit("192.168.1.0/24") -> 192.168.1.1-255
        @api.iplimit("0.0.0.0/0") -> all ip address
    """

    def decorator(function: Callable) -> Callable:
        """函数包装器"""

        networks = [ipaddress.ip_network(addr) for addr in allowed]

        def wrapper(*args, **kwargs) -> object:
            """参数包装器"""

            # 获取地址
            address = ipaddress.ip_address(_request.remote_addr)

            # 判断地址
            for network in networks:
                if address in network:
                    return function(*args, **kwargs)

            return _abort(403)

        # 重命名函数防止 overwriting existing endpoint function
        wrapper.__name__ = function.__name__

        return wrapper
    return decorator


def require(pointname: str, checkuser: bool = False) -> Callable:
    """
    一个权限验证装饰器:
        pointname: 需要的权限点名称
        checkuser: 是否获取用户给视图层处理:
            0. 如果未启用按照正常的权限验证流程处理(即权限不足时403)
            1. 如果启用了在权限验证不足时会:
                0. 设置 g.operator: str - 通过数据库查询的用户信息
                1. 设置 g.checkuser: bool = True
                1. 将权限交予视图层函数处理

        0. 通过 flask 获取 Bearer-Token 并验证用户的 JWT Token 是否合法
        1. 通过 accesspoint 查询数据库所需要的访问级别
        2. 如果可以访问返回函数值否则返回 403
    """

    def decorator(function: Callable) -> Callable:
        """函数包装器"""

        def wrapper(*args, **kwargs) -> Any:
            """参数包装器"""

            # 验证 token 是否正确
            try:
                payload: dict = validator.jwttoken()
            except error.Error as _error:
                logger.warning(_error)
                return settings.Authorization.UnAuthorized(_error)
            _g.checkuser: bool = False
            _g.operator = payload.get(rbac.jwt.const.Payload.Audience)

            # 检查用户权限是否符合要求
            try:
                diff: int = validator.permission(pointname, payload)
            except bson.errors.InvalidId as _error:
                logger.warning(_error)
                return settings.Authorization.UnAuthorized(_error)
            except rbac.error.AccessPointNotFound as _error:
                logger.warning(_error)
                if not settings.Authorization.ExecuteAPMissing:
                    return settings.Authorization.NotPermitted(_error)
                return function(*args, **kwargs)
            else:
                # 如果权限符合 - 直接返回
                # 如果权限不符合但是需要检查userid - 同样返回
                if not diff or checkuser:
                    _g.checkuser = checkuser
                    return function(*args, **kwargs)

                # 如果不需要手动检查userid, 权限也不正确则返回403
                return settings.Authorization.NotPermitted(str(diff))

        # 重命名函数防止 overwriting existing endpoint function
        wrapper.__name__ = function.__name__
        return wrapper
    return decorator


def wrap(payload: str) -> Callable:
    """
    一个API接口装饰器:
        执行函数获取返回值
        判断函数执行是否发生错误
        如果发生错误则返回错误信息
    payload - 要在数据包内放置数据的键
    """

    def decorator(function: Callable) -> Callable:
        """函数包装器"""

        def wrapper(*args, **kwargs) -> object:
            """参数包装器"""

            response = dict()

            # 尝试执行函数
            try:
                result = function(*args, **kwargs)

            except error.Error as _error:
                # 发生内部错误
                response[settings.Response.Code] = _error.code
                response[settings.Response.Message] = _error.message()
                response[settings.Response.Description] = _error.description
                logger.error(_error)

            except HTTPException as _error:
                # 主动抛出 HTTP 错误
                return _error

            # pylint: disable=broad-except
            except Exception as _error:
                # 发生未定义错误
                code = settings.Response.Codes.Unknown
                description = settings.Response.Descriptions.Unknown
                response[settings.Response.Code] = code
                response[settings.Response.Message] = str(_error)
                response[settings.Response.Description] = description

                # 保存堆栈信息
                exenvior = sys.exc_info()
                exstr = traceback.format_exception(*exenvior)
                exstr = ''.join(exstr)
                logger.error(exstr)

            else:
                # 未发生错误时 - 如果是 Response 类 直接返回
                if isinstance(response, _Response):
                    return response

                # 如果是普通数据
                response[settings.Response.Code] = settings.Response.Codes.Success
                response[settings.Response.Message] = settings.Response.Messages.Success
                response[settings.Response.Description] = settings.Response.Descriptions.Success
                response[payload] = result

            return jsonify(response)

        # 重命名函数防止 overwriting existing endpoint function
        wrapper.__name__ = function.__name__

        return wrapper
    return decorator
