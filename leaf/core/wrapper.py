"""Leaf 装饰器函数库"""

import time
import queue
import threading

from typing import Callable, NoReturn


def thread(function: Callable) -> object:
    """制造一个新线程执行指定任务"""

    def params(*args, **kwargs):
        """接受任务函数的参数"""

        # 通过线程执行函数
        def process(*args, **kwargs):
            """过程函数包装"""
            function(*args, **kwargs)

        _thread = threading.Thread(
            target=process, args=args, kwargs=kwargs)
        _thread.setDaemon(True)
        _thread.start()

    return params


def timer(function: Callable) -> object:
    """计时函数 - 执行之后显示执行时间"""

    def wrapper(*arg, **kwargs):
        """参数接收器"""
        # 计时并执行函数
        start = time.time()
        result = function(*arg, **kwargs)
        end = time.time()

        # 显示时间
        used = (end - start) * 1000
        print("-> elapsed time: %.2f ms" % used)
        return result

    return wrapper


def timelimit(limited: float) -> object:
    """
    限制一个函数的执行时间:
        1. 创建两个线程 - 计数器 + 工作线程
        2. 通过一个 threading.Lock 的锁同步工作状态
        3. 如果锁释放了则判断工作是否完成

    *注意: 这种方法在超时之后会触发 TimeoutError
    *注意: 但是并不会影响工作线程的工作 - 工作线程无法被动结束
    """

    def wrapper(function: Callable):
        """函数包装器"""
        # 初始化锁, 队列变量
        result = queue.Queue(maxsize=1)
        mutex = threading.Lock()
        mutex.acquire()

        def _timer_work() -> NoReturn:
            """需要计时器到时之后释放锁"""
            mutex.release()

        def params(*args, **kwargs):
            """参数接收器"""

            def _worker_work(*args, **kwargs):
                """任务工作线程"""
                result.put(function(*args, **kwargs))
                # 检查并尝试释放锁
                # pylint: disable=no-member
                if mutex.locked():
                    mutex.release()

            # 设置定时器 + 工作线程
            _timer = threading.Timer(limited, _timer_work)
            _worker = threading.Thread(
                target=_worker_work, args=args, kwargs=kwargs)
            _worker.setDaemon(True)
            _worker.start()
            _timer.start()

            # 尝试获取锁变量之后检查任务状态
            if mutex.acquire():
                _timer.cancel()

                # 如果任务已经完成 - 返回结果
                if not result.empty():
                    return result.get()
                # 如果任务未完成 - 触发超时
                raise TimeoutError

            return result.get_nowait()

        return params
    return wrapper
