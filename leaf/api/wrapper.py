"""API 函数的包装器"""

import sys
import json
import types
import logging
import datetime
import ipaddress
import traceback
from typing import Callable, Type, Dict, NoReturn, Optional, Iterable

from flask import abort
from flask import request
from flask import Response

from bson import ObjectId
from werkzeug.exceptions import HTTPException

from . import settings
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
converter.register(ObjectId, str)
converter.register(datetime.datetime, lambda obj: obj.isoformat())
converter.register(datetime.time, lambda obj: obj.isoformat)
converter.register(Exception, str)


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
    return Response(
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
            address = ipaddress.ip_address(request.remote_addr)

            # 判断地址
            for network in networks:
                if address in network:
                    return function(*args, **kwargs)

            return abort(403)

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
                if isinstance(response, Response):
                    return response

                # 如果是普通数据
                response[settings.Response.Code] = \
                    settings.Response.Codes.Success
                response[settings.Response.Message] = \
                    settings.Response.Messages.Success
                response[settings.Response.Description] = \
                    settings.Response.Descriptions.Success
                response[payload] = result

            return jsonify(response)

        # 重命名函数防止 overwriting existing endpoint function
        wrapper.__name__ = function.__name__

        return wrapper
    return decorator
