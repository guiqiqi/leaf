"""
插件支持模块:
    current - 当前的插件目录
    manager - 插件管理器
    settings - 插件相关设置
"""

from os import path as __path

# 获取当前目录生成插件管理器
from .manager import Manager
from . import settings
current = __path.split(__path.realpath(__file__))[0]
