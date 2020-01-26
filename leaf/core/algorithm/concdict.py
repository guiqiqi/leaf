"""一个线程安全的阻塞字典"""

import threading
from typing import Hashable, Dict, NoReturn, Optional


class ConcurrentDict:
    """该字典当要pop的键不存在时, 会阻塞操作线程"""

    def __init__(self):
        self.__events: Dict[Hashable, threading.Event] = dict()  # 用于存储键和查询锁对
        self.__data: Dict[Hashable, object] = dict()  # 用于存储键值对

    def put(self, key: Hashable, value: object):
        """
        向键值对中加入存储
            该函数会检查 key 是否在 self.events 里
            当存在时则说明有某些查询操作正在被阻塞, 此时需要对该
            锁进行 set 操作, 通知对应的线程们取走数据
        """
        # 检验字典键是否可 hash 并存储值
        self.__data[key] = value

        # 设置事件 - 释放线程的阻塞状态
        if key in self.__events.keys():
            event = self.__events.pop(key)
            if not event.isSet():
                event.set()

    def get(self, key: Hashable, timeout: Optional[int] = None) -> object:
        """
        从存储中返回值:
            该函数会首先检查 self.data 中是否有对应的键
            如果有则直接返回
            否则在 self.events 中新建一个 threading.Event
            对象并将其 clear, 之后进行 wait 操作阻塞线程
            当 put 操作加入对应的键值对时, 该 event 对象
            会被 set, 此时对应的阻塞释放, 返回相应的值

        *timeout: 超时时长, 超时之后触发 TimeoutError, 默认为无限大
        """
        # 检验字典键是否可 hash 并检查值是否已经存在
        # assert(isinstance(key, Hashable))
        if key in self.__data.keys():
            return self.__data.pop(key)

        # 判断是否已经有 Event 对象被创建, 如有则不创建
        event = threading.Event()
        event.clear()
        if not key in self.__events.keys():
            self.__events[key] = event
        else:
            event = self.__events[key]

        # 阻塞等待线程
        event.wait(timeout)

        # 当超时或者获取到之后
        if key in self.__data.keys():
            return self.__data[key]
        raise TimeoutError("key '%s' not found" % key)

    def erase(self, key: Hashable) -> NoReturn:
        """从存储中移除对应的键值对"""

        # assert(isinstance(key, Hashable))
        if key in self.__data.keys():
            self.__data.pop(key)
