"""Leaf 任务计划与调度"""

import uuid
import time
import threading

from typing import Dict, Callable, Optional, Generator, NoReturn

# 时间间隔常量定义
MINUTE = 60  # 分钟间隔
HOUR = MINUTE * 60  # 小时间隔
DAY = HOUR * 24  # 每天间隔
WEEK = DAY * 7  # 一周间隔
MONTH = DAY * 30  # 每月间隔


class Worker:
    """工作任务类"""

    def __repr__(self) -> str:
        """返回 repr 信息"""
        return "<Leaf ScheduleWorker>"

    def __init__(self, task: Callable[[], object], interval: float,
                 runtimes: Optional[int] = 0, id_: Optional[str] = None,
                 fineness: Optional[float] = 1):
        """
        任务类初始化函数
        task: 需要运行的任务函数 - 需要经过包装(无参)
        interval: 每次运行的时间间隔
        runtimes: 可以指定任务运行指定次数后终止 - 默认为0 - 无限次
        id: 需要时可以手动指定该任务的id - 默认为自动生成
        fineness: 检查任务是否终止的细度 - 默认为1s
        """
        # 保存任务信息
        self.__task = task
        self.__interval = interval
        self.__fineness = fineness

        # 初始化任务变量
        self.__status = False  # 任务是否在运行
        self.__runtimes = runtimes  # 已经运行过的次数
        # self.__results = queue.Queue()  # 任务返回值存储
        if id_ is None:
            self.__id = uuid.uuid1().hex
        else:
            self.__id = id_

    def _blocker(self) -> Generator:
        """
        使用 yield 关键字实现协程间隔:
            每次的阻塞过程分成许多个最小单位
            每个最小单位的阻塞时间为 self.__fineness
            之后检测是否已经阻塞足够长时间 + 是否被取消任务:
                如果足够 - 运行任务
                不够 - 继续休眠
                被取消 - 终止
        """
        # 记录总的休眠时间
        gap: float = self.__interval

        while self.__status:
            # 如果休眠时长足够
            if gap <= 0:
                gap = self.__interval
                yield

            # 否则继续休眠
            time.sleep(self.__fineness)
            gap -= self.__fineness

    def _do(self) -> NoReturn:
        """
        任务包装的运行函数:
            通过循环 + 阻塞器实现
            当任务次数达到之后设置运行标志位为 False
            则会在下一次运行时退出循环
        """
        # 初始化阻塞器
        runtimes = self.__runtimes
        blocker = self._blocker()

        # 检测任务状态
        while self.__status:

            # 检测运行次数是否达到
            runtimes -= 1
            if runtimes == 0:
                self.stop()

            # 执行任务
            # self.__results.put(self.__task())
            self.__task()

            # 进行任务休眠 - 休眠失败则退出执行
            try:
                blocker.send(None)
            except StopIteration as _error:
                break

        blocker.close()

    def start(self) -> NoReturn:
        """设置任务启动标志位并启动任务线程"""
        # 如果已经启动
        if self.__status is True:
            return

        # 如果还未启动 - 初始化线程并启动
        self.__status = True
        worker = threading.Thread(target=self._do)
        worker.setDaemon(True)
        worker.start()

    def stop(self) -> NoReturn:
        """设置任务终止标志位"""
        self.__status = False

    @property
    def interval(self) -> float:
        """返回任务间隔时长"""
        return self.__interval

    @interval.setter
    def interval(self, new: float) -> NoReturn:
        """重设任务间隔时长 - 下次运行时生效"""
        self.__interval = new

    @property
    def id(self) -> str:
        """返回任务id"""
        return self.__id


class Manager:
    """通过字典来实现任务管理与记录"""

    def __repr__(self) -> str:
        """返回 repr 信息"""
        return "<Leaf ScheduleManager>"

    def __init__(self, disable: Optional[bool] = False):
        """
        通过保存一个字典来记录任务类
        disable 变量设置为 True 时不允许任何计划任务运行
        """
        self.__disable = disable
        self.__tasks: Dict[str, Worker] = dict()

    def get(self, id_: str) -> Worker:
        """根据任务 id 获取任务类"""
        return self.__tasks.get(id_)

    def start(self, worker: Worker) -> NoReturn:
        """新增一个工作类实例并启动该任务"""
        self.__tasks[worker.id] = worker

        # 检测到有其他进程运行任务时不运行任务
        if not self.__disable:
            worker.start()
