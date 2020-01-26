"""Leaf 连接池实现"""

import queue
from typing import Callable, Optional, NoReturn

# 自定义的数据库驱动模块
import pymongo

from . import wrapper


class Pool:
    """一个通用连接池实现"""

    def __repr__(self) -> str:
        """返回repr信息"""
        return "<Leaf-DBPool>"

    def __init__(self, size: int,
                 creator: Callable[[], object],
                 closer: Callable[[object], NoReturn],
                 timeout: Optional[float] = 0):
        """
        连接池初始化函数实现:
            size: 连接池默认空闲连接
            creator: 创建连接函数
            closer: 关闭连接函数
            timeout: 连接超时函数 - 默认为0: 不超时
        """

        # 通过 queue 来给出最空闲的连接
        self.__size = size
        self.__pool = queue.Queue(maxsize=size)

        # 构造创建函数 - 当不超时时
        if timeout <= 0:
            @wrapper.thread
            def _creator():
                self.__pool.put(creator())
            self.creator = _creator

        # 当设置超时 - 使用 timeout 计时器
        else:
            @wrapper.timelimit(timeout)
            def _creator():
                self.__pool.put(creator())
            self.creator = _creator

        # 构造关闭函数
        self.closer = closer

        # 初始化连接
        for _index in range(size):
            self.creator()

    def __del__(self):
        """析构时关闭所有链接"""
        self.stop()

    def stop(self) -> NoReturn:
        """
        关闭所有链接
        """
        while self.__pool.qsize():
            self.closer(self.__pool.get())

    def get(self) -> object:
        """获取一个数据库连接"""
        connection = self.__pool.get()
        return connection

    def put(self, connection: object) -> NoReturn:
        """归还一个数据库连接"""
        self.__pool.put(connection)

    def status(self) -> float:
        """返回当前连接池的忙碌状态"""
        return 1 - self.__pool.qsize() / self.__size


class MongoDBPool(Pool):
    """MongoDB 数据库连接池 - 继承自连接池"""

    @staticmethod
    def _create_connection(server: str, port: int, username: str,
                           password: str, timeout: float, **optional) -> pymongo.MongoClient:
        """
        创建一个 MongoDB 链接的静态函数:
            server: 数据库地址
            port: 数据库端口
            username: 用户名
            password: 密码
            timeout: 超时时间按照毫秒计算
            **optional: 可选项, 会被传递给 pymongo 驱动
        """
        return pymongo.MongoClient(
            server, port, username=username,
            password=password, **optional,
            serverSelectionTimeoutMS=timeout
        )

    @staticmethod
    def _close_connection(connection: pymongo.MongoClient) -> NoReturn:
        """关闭一个 MongoDB 的链接"""
        connection.close()

    def __init__(self, size: int, server: str, port: int,
                 username: str, password: str, timeout: float, **optional):
        """
        重写 Pool 的初始化函数
        *注意: timeout - 按照秒计算的超时时间
        *注意: database - 返回的直接选择的数据库
        *注意: **optional - 会被直接传递给 pymongo 驱动
        """

        # 创建连接与选择器函数包装
        def creater() -> pymongo.MongoClient:
            return self._create_connection(
                server, port, username, password,
                timeout * 1000, **optional)

        closer = self._close_connection

        # 初始化父类函数
        super().__init__(size, creater, closer, timeout)

    def version(self):
        """获取数据库版本"""
        connection = super().get()
        version = connection.server_info.get("version", "unknwon")
        super().put(connection)
        return version

    def get(self) -> pymongo.MongoClient:
        """获取一个数据库对象"""
        connection = super().get()
        return connection
