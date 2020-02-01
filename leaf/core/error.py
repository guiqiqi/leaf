"""Leaf 异常定义与处理模块"""

import sys
import json
import logging

from typing import Optional, IO


# Leaf 系统使用的最小/最大错误码
MIN_LEAF_ERRCODE = 10000
MAX_LEAF_ERRCODE = 19999

# 默认错误消息格式
_ERROR_MSG_FORMAT = \
    """
错误代码: {code}
错误描述: {desc}
错误消息: {message}
"""

# 无错误消息时的填充信息
_DEFAULT_ERROR_MSG = "无"

# 默认的错误记录格式
_DEFAULT_RECORD_FORMAT = \
    (
        "%(asctime)s - logger %(name)s\n"
        "%(pathname)s:%(funcName)s:%(lineno)s\n"
        "%(levelname)s in %(threadName)s: %(message)s"
    )


class Error(Exception):
    """
    Leaf 中所有的错误都需要从此继承:
        错误代码约定:
        所有的错误代码由五位数字组成 - 10000 - 99999
        其中 10000 - 19999 由 Leaf 框架使用
        其余的可以由开发者自行定制

    当一个类继承了 leaf.core.error.Error 之后
    需要:
        定义其错误代码 - 静态成员变量 code
        定义其错误描述 - 静态成员变量 description
    """
    code = 0  # 错误根类的错误代码为 0
    description = "System Error"  # 默认的系统错误消息

    def __init__(self, message: Optional[str] = None):
        """
        错误构造函数:
            message: 错误消息 - 选填
        """
        if message is None:
            message = _DEFAULT_ERROR_MSG
        self.__msg = message
        super().__init__(self.__msg)

    def __format(self) -> str:
        """格式化错误消息并返回"""
        return _ERROR_MSG_FORMAT.format(
            code=self.code,
            desc=self.description,
            message=self.__msg
        )

    def message(self) -> str:
        """返回错误消息"""
        return self.__msg

    def __repr__(self) -> str:
        """为解释器调试重载 repr 函数"""
        return self.__format()

    def __str__(self) -> str:
        """为文档输出重载 str 函数"""
        return self.__format()

    def __int__(self) -> int:
        """int 错误对象会直接返回错误代码"""
        return int(self.code)


class Messenger:
    """
    错误消息管理器
    错误消息有两种定义方式:
        1. 按照错误类规定存储在 json 格式的文件内, 示例格式:
            {
                "20001": "这是一条测试错误消息",
                ...
            }
        之后使用 Messenger.load 函数注册到类实例中

        2. 直接定义错误类 - 继承自 leaf.core.error.Error
        之后使用 Messenger.register 函数注册到类实例中
    """

    def __repr__(self) -> str:
        """返回 repr 信息"""
        return "<Leaf ErrorMessenger>"

    def __init__(self):
        """错误消息管理器构造函数"""
        self.__registry: dict = dict()

    def register(self, _error: Error):
        """
        向错误消息管理器中注册一个错误消息:
            _error: Error 类
        函数会尝试从 Error 类中读取:
            _error.code, _error.description 信息
            并将其注册到本地的 registry 中
        """
        self.__registry[int(_error.code)] = _error.description

    def load(self, handler: IO):
        """
        使用 json 文件向消息管理器批量注册错误代码与消息:
            handler: IO 类 - 应该为已经打开的文件 IO
            函数会尝试从中读取错误消息 - 按照上面的 json 文件规定
            推荐使用 leaf.core.tools.file.read 函数获取 IO
        """
        kvmap: dict = json.load(handler)
        for keycode, desc in kvmap.items():
            self.__registry[int(keycode)] = desc

    def get(self, code: int) -> str:
        """
        通过给定的错误代码寻找错误信息:
            code: 已经注册的错误代码
        *注意: 当未找到对应的错误消息时会引发 KeyError 错误
        """
        return self.__registry[code]

    def all(self) -> dict:
        """
        返回所有的错误信息
        """
        return self.__registry

    def error(self, code: int, message: Optional[str] = '') -> Error:
        """
        当错误是以 code 方式直接 load 时
        制作一个 Error 并返回
        """
        description = self.__registry.get(code)

        error = Error(message)
        error.code = code
        error.description = description

        return error


class Logging:
    """
    使用 logging 模块的日志记录器

    主 Logger 名称为 leaf
    模块请使用 logging.getLoggger("leaf.xxx")
    获取 Logger - 这样可以保持全局的设置一致
    获取到子 logger 后可以改写设置
    """

    def __repr__(self) -> str:
        """返回 repr 信息"""
        return "<Leaf ErrorLogging>"

    def __init__(self, file: Optional[str] = None,
                 stream: Optional[IO] = sys.stdout,
                 fmt: Optional[str] = _DEFAULT_RECORD_FORMAT):
        """
        初始化错误记录器
            stream: 要输出的流位置 - 默认 sys.stderr
            file: 要输出的日志文件 - 默认不输出
            format: 要输出的格式 - 默认配置
        """
        self.__logger = logging.getLogger("leaf")
        self.__formatter = logging.Formatter(fmt)

        # 生成流记录器并设置格式添加至主记录器
        self.__console_handler = logging.StreamHandler(stream)
        self.__console_handler.setFormatter(self.__formatter)
        self.__logger.addHandler(self.__console_handler)

        # 生成文件记录器
        if not file is None:
            self.__file_handler = logging.FileHandler(file)
            self.__file_handler.setFormatter(self.__formatter)
            self.__logger.addHandler(self.__file_handler)

    @property
    def logger(self) -> logging.Logger:
        """返回 leaf 主日志记录器"""
        return self.__logger

    @property
    def file_handler(self) -> logging.Handler:
        """返回文件记录 Handler"""
        return self.__file_handler

    @property
    def console_handler(self) -> logging.Handler:
        """返回流记录 Handler"""
        return self.__console_handler
