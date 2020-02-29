"""
Leaf 框架核心部分:
    tools - 常用的工具函数库封装
    algorithm - 常用的数据结构算法封装

    error - 错误与日志记录
    events - 一个事件管理器
    wrapper - 常用的装饰器封装
    database - 提供一个连接池模块+MongoDB连接池
    schedule - 提供一个任务计划调度模块

    modules - 一个用于保存运行时实例的字典
"""

from . import tools
from . import abstract
from . import algorithm

# modules 保存 Leaf 框架运行时实例
modules = algorithm.AttrDict()

# pylint: disable=wrong-import-position
from . import error
from . import events
from . import wrapper
from . import database
from . import schedule
from . import parallel
