"""并行支持尝试 - 废弃"""

from typing import Union as _Union
from typing import Tuple as _Tuple
from typing import Hashable as _Hashable
from typing import Optional as _Optional
from typing import NoReturn as _NoReturn

from multiprocessing import current_process as _current_proc
from multiprocessing.managers import Namespace as _Namespace
from multiprocessing.managers import SyncManager as _Manager
from multiprocessing.managers import BaseProxy as _BaseProxy
from multiprocessing.managers import NamespaceProxy as _NamespaceProxy


from . import algorithm


class AttributeProxy(_BaseProxy):
    """
    继承自 BaseProxy 为 AttrDict 使用的多进程代理
    重载 __getattr__ 与 __setattr__ 与 __repr__
    当需要获取的 attribute 字符串以 '_' 开始时从类内获取
    否则调用 BaseProxy 的 _callmethod 函数调用
    """
    _exposed_ = (
        "__getattr__", "__setattr__", "__getitem__", "__setitem__",
        "keys", "fromkeys", "values", "setdefault", "update", "get",
        "clear", "popitem", "copy", "items", "pop"
    )

    def __getitem__(self, key: _Hashable) -> object:
        """返回对象指定索引切片的拷贝"""
        return super()._callmethod("__getitem__", args=(key,))

    def __setitem__(self, key: _Hashable, value: object) -> _NoReturn:
        """返回对象指定索引切片的拷贝"""
        return super()._callmethod("__setitem__", args=(key, value))

    def __getattr__(self, methodname: str) -> object:
        """查询是否是 '类内对象' 并返回"""
        if methodname.startswith('_'):
            return super().__getattribute__(methodname)

        return super()._callmethod("__getitem__", args=(methodname, ))

    def __setattr__(self, name: str, value: object) -> _NoReturn:
        """查询是否是 '类内对象' 并设置"""
        if name.startswith('_'):
            return super().__setattr__(name, value)

        return super()._callmethod("__setitem__", args=(name, value))

    def __repr__(self):
        """返回对象的 __repr__ 对象, 隐藏代理属性"""
        return super().__str__()


class Modules:
    """
    通过多进程 Manager.Namespace
    使用代理 AttrDict 的修改操作
    """

    def __init__(self, space: _Namespace):
        """在 space 中保存数据容器"""
        self.__space = space
        container = algorithm.AttrDict()
        self.__space.modules = container

    def __repr__(self) -> str:
        """显示数据容器 AttrDict 的 repr 值"""
        return repr(self.__space.modules)

    def __setattr__(self, key: _Hashable, value: object) -> _NoReturn:
        """代理 setattr 操作"""
        if key == "_Modules__space":
            super().__setattr__(key, value)
            return

        _modules = self.__space.modules
        _modules.__setattr__(key, value)
        self.__space.modules = _modules

    def __getattr__(self, key: _Hashable) -> object:
        """代理 getattr 操作"""
        if key == "_Modules__space":
            # pylint: disable=no-member
            return super().__getattr__(key)

        _modules = self.__space.modules
        return _modules.__getattr__(key)

    def __setitem__(self, key: _Hashable, value: object) -> _NoReturn:
        """重定向到 setattr 操作"""
        self.__setattr__(key, value)

    def __getitem__(self, key: _Hashable) -> object:
        """重定向至 getattr 操作"""
        return self.__getattr__(key)


class Master:
    """
    管理服务器端进程 - 仅需要启动一次
    会创建一个共享资源服务器，用于在不同进程之间共享变量:
        start - 启动管理端进程, 返回服务器地址
        connect(staticmethod) - 连接到远程管理器
        shutdown(staticmethod) - 关闭管理进程
    """

    def __init__(self, address: _Optional[_Tuple[str, int]] = None,
                 authkey: _Optional[str] = None):
        """
        初始化管理进程
            address: 可选, 当未给定时使用文件描述符
            authkey: 可选, 用于认证远程连接

        初始化命名空间与 modules 变量
        """
        if isinstance(authkey, str):
            authkey = authkey.encode()

        self.__namespace = _Namespace()
        self.__modules = algorithm.AttrDict()
        self.__manager = _Manager(address=address, authkey=authkey)

        # 初始化项目共享变量
        self.__namespace.version = "version"

        # pylint: disable=no-member
        self.__manager.register("namespace", callable=self.namespace,
                                proxytype=_NamespaceProxy)
        self.__manager.register("modules", callable=self.modules,
                                proxytype=AttributeProxy)
        self.__manager.register("attrdict", callable=algorithm.AttrDict,
                                proxytype=AttributeProxy)

        _current_proc().authkey = authkey

    def start(self) -> _Union[tuple, str]:
        """
        启动管理服务
        返回管理服务器地址
        """
        # pylint: disable=no-member
        self.__manager.start()
        # self.blocking()

        return self.__manager.address

    def namespace(self) -> _NamespaceProxy:
        """返回命名空间"""
        return self.__namespace

    def modules(self) -> AttributeProxy:
        """返回包管理器代理"""
        return self.__modules

    def manager(self) -> _Manager:
        """返回管理器对象"""
        return self.__manager

    @staticmethod
    def connect(address: _Union[str, tuple],
                authkey: _Optional[bytes] = None) -> _Manager:
        """
        连接到一个远程服务器
            address: 远程服务器的地址+端口/sock文件
            authkey: 可选, 如果需要身份验证密钥
        """
        # pylint: disable=no-member
        connection = _Manager(address=address, authkey=authkey)
        connection.register("namespace", proxytype=_NamespaceProxy)
        connection.register("modules", proxytype=AttributeProxy)
        connection.register(
            "attrdict", proxytype=AttributeProxy)
        connection.connect()
        _current_proc().authkey = authkey
        return connection

    @staticmethod
    def blocking():
        """产生阻塞"""
        __import__("queue").Queue().get()
