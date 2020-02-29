"""
并行支持尝试 - 新版

模型会通过尝试获取独占锁的方式来检查
是否有别的 Leaf 进程正在运行
当没有检测到的时候 - 该进程工作为 Master(主调度进程)
当检测到的时候 - 该进程工作为 Slave(从属进程)

从属进程不需要运行 Schedule 任务调度管理器
其所有的任务调度全部不执行(因为主进程执行一次即可)

从属进程的 Event 事件系统拥有 async 参数
它指代这个事件是否需要通知到其他的进程执行
"""

from typing import IO as _IO
from typing import Dict as _Dict
from typing import List as _List
from typing import NoReturn as _NR
from typing import Tuple as _Tuple
from typing import Union as _Union
from typing import Optional as _Optional

import os as _os
import atexit as _atexit
import multiprocessing as _mp
import multiprocessing.managers as _managers


class Detector:
    """
    调度进程检测模型:
    通过使用 fcntl 的 EX|NB 建议排他锁来检测
    是否有其余的 Leaf 进程正在执行

    如果当前进程为 Matser 角色
    会在给定的检测文件中写入调度器链接地址
    """

    def __init__(self, filename: str) -> _NR:
        """
        调度进程模型 - 初始化锁环境
        通过尝试获取独占锁而检测是否有其余的进程
            filename: 锁文件名
        """

        # 检查是否可以调用 fcntl 库
        try:
            import fcntl as _locker
        except ImportError as _error:
            raise EnvironmentError("Windows not support fcntl")

        # 检测 locker 文件是否存在
        if not _os.path.isfile(filename):
            open(filename, 'w').close()

        # 初始化进程 pid 文件 handler
        self.__locker_filename: str = filename
        handler = open(filename, 'r+')
        self.__locker_handler: _IO = handler
        _atexit.register(self.__locker_handler.close)

        # 通过尝试获取独占锁进行测试
        try:
            mode: int = _locker.LOCK_EX | _locker.LOCK_NB
            _locker.flock(self.__locker_handler, mode)
        except IOError as _error:
            self.__is_master = False
        else:
            self.__is_master = True
            handler.truncate()
            unmode: int = _locker.LOCK_UN
            _atexit.register(lambda: _locker.flock(handler, unmode))

    @property
    def locker(self) -> _IO:
        """返回文件锁句柄"""
        return self.__locker_handler

    @property
    def master(self) -> bool:
        """返回是否是主调度进程"""
        return self.__is_master


class Controller:
    """
    管理服务器端进程 - 仅需要启动一次
    会创建一个共享资源服务器，用于在不同进程之间共享变量:
        start - 启动管理端进程, 返回服务器地址
        connect(staticmethod) - 连接到远程管理器
    """

    def __init__(self, address: _Union[_Tuple[str, int], str],
                 authkey: _Union[str, bytes],
                 maxsize: _Optional[int] = 128) -> _NR:
        """
        初始化管理进程
            address: 管理器地址
            authkey: 管理器连接密钥
            maxsize: 可选, 用于设置任务队列的最大长度

        初始化命名空间与环境变量
            workers: 工作进程 PID 与其对应任务队列的映射
            namespace.master: 控制进程的 PID
            namespace.workers: 当前的总工作进程数
        """
        if isinstance(authkey, str):
            authkey = authkey.encode()

        self.__maxsize: int = maxsize
        self.__workers: _Dict[int, _mp.Queue] = dict()
        self.__namespace = _managers.Namespace()
        self.__namespace.master: int = _os.getpid()
        self.__namespace.workers: _List[int] = list()

        # 初始化管理器
        self.__manager = _managers.SyncManager(
            address=address, authkey=authkey)

        # pylint: disable=no-member
        self.__manager.register("bind", callable=self.__register)
        self.__manager.register("unbind", callable=self.__unregister)
        self.__manager.register("boardcast", callable=self.__boradcast)
        self.__manager.register(
            "namespace", callable=self.__get_namespace,
            proxytype=_managers.NamespaceProxy)

    def start(self) -> _Union[_Tuple[str, int], str]:
        """启动调度服务器"""
        # pylint: disable=no-member
        self.__manager.start()
        return self.__manager.address

    @property
    def address(self) -> _Union[_Tuple[str, int], str]:
        """返回管理器地址"""
        # pylint: disable=no-member
        return self.__manager.address

    def __get_namespace(self) -> _managers.Namespace:
        """返回当前命名空间对象"""
        return self.__namespace

    def __boradcast(self, eventname: str, *args, **kwargs) -> _NR:
        """
        广播一个事件 - 三元组:
            0. 事件名称
            1. 事件位置参数
            2. 事件关键字参数
        *注意: 给定的参数必须可以序列化
        """
        for _pid, queue in self.__workers.items():
            queue.put((eventname, args, kwargs))

    def __register(self, pid: int) -> _mp.Queue:
        """注册一个进程到管理器"""
        self.__namespace.workers.append(pid)
        self.__workers[pid] = _mp.Queue(self.__maxsize)
        return self.__workers[pid]

    def __unregister(self, pid: int) -> _NR:
        """解注册一个进程"""
        self.__workers.pop(pid, None)

    @staticmethod
    def connect(address: _Union[_Tuple[str, int], str],
                authkey: _Union[str, bytes]) -> _mp.managers.SyncManager:
        """
        连接到一个远程服务器:
            address: 远程服务器的地址+端口/sock文件
            authkey: 管理服务器的验证密钥
        """
        if isinstance(authkey, str):
            authkey = authkey.encode()

        # pylint: disable=no-member
        connection = _managers.SyncManager(address=address, authkey=authkey)
        connection.connect()
        connection.register("namespace", proxytype=_managers.NamespaceProxy)
        if not "bind" in dir(connection):
            connection.register("bind")
            connection.register("unbind")
            connection.register("boardcast")
        return connection
