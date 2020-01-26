"""插件管理器类"""

import logging
from threading import Thread
from types import ModuleType
from typing import NoReturn, Dict, Iterable, Optional
from collections import namedtuple
from importlib import reload as pyreload

from . import error
from . import settings
from ..core.tools import file
from ..core.abstract.plugin import Plugin

# 载入模块的返回值
LoadedPlugin = namedtuple("LoadedPlugin", ("plugin", "module"))
logger = logging.getLogger("leaf.plugins")

class Manager:
    """
    插件管理器类:
        start: 启动一个插件
        stop: 停止一个插件
        unload: 卸载一个插件
        reload: 重载一个插件
        scan: 扫描是否有新的插件
        clean: 清理已经失效的插件
    """

    def __repr__(self) -> str:
        """返回 repr 信息"""
        return "<Leaf PluginManager with directory '%s'>" % self.__directory

    def __init__(self, directory: str):
        """
        插件注册器类构造函数
            directory: 要扫描的插件目录
        """
        # 扫描插件的目录
        self.__directory: str = directory
        # 插件 ID 与 import 之后 module 的映射
        self.__modules: Dict[str, ModuleType] = dict()
        # 插件 ID 与 生成的插件实例的映射
        self.__plugins: Dict[str, Plugin] = dict()
        # 插件 ID 与载入目录 catalog 的映射
        self.__catalogs: Dict[str, str] = dict()
        # 插件 ID 与对应顶级域 domain 的映射
        self.__domains: Dict[str, Plugin] = dict()

    @staticmethod
    def __load(catalog: str) -> LoadedPlugin:
        """
        尝试从一个目录载入插件:
            catalog: 要尝试的插件目录
        LoadedPlugin.plugin - 载入的插件
        LoadedPlugin.module - 载入的模块
        """
        try:
            # __import__ 函数的 level 设置为 1 可以不污染全局目录
            module = __import__(catalog, globals(), locals(), [], 1)
            plugin = module.plugin
            result = LoadedPlugin(plugin, module)
        except ImportError as _error:
            # 当有载入错误时
            raise error.PluginImportError(_error)
        except AttributeError as _error:
            # 当插件不符合规范时
            raise error.PluginInitError(_error)
        except Exception as _error:
            # 插件运行期间错误
            raise error.PluginRuntimeError(_error)

        return result

    @staticmethod
    def __reload(module: ModuleType) -> ModuleType:
        """
        重新载入一个模块并返回:
            module: 需要重新载入的模块
        """
        newmodule = pyreload(module)
        del module
        return newmodule

    @staticmethod
    def __scandirs(target: str, skipped: set) -> set:
        """
        目录扫描函数:
            target: 要扫描的文件夹地址
            skipped: 要跳过扫描的地址
        """

        result = set()
        catalogs = file.dirs(target)

        for catalog in catalogs:
            # 跳过不要扫描的地址
            if catalog in skipped:
                continue
            result.add(catalog)

        return result

    def register(self, plugin: Plugin, domains: Iterable) -> NoReturn:
        """
        向管理器注册插件的顶级域:
            pluginid: 插件的 id
            domains: 要注册的顶级域列表
        """
        for domain in domains:
            self.__domains[domain] = plugin

    def domain(self, domain: str) -> Plugin:
        """
        根据传入的顶级域返回对应的插件:
            domain: 要搜索的顶级域字符串

        *注意:
        当找不到对应插件时会返回 None
        当传入顶级域对应的插件已经停止运行时仍然会返回 None
        """
        plugin: Plugin = self.__domains.get(domain)
        if plugin and plugin.status is True:
            return plugin
        return None

    def id(self, pluginid: str) -> Plugin:
        """
        返回 id 对应的插件
            pluginid: 要搜索的插件 id

        *注意:
        当找不到对应插件时会返回 None
        """
        return self.__plugins.get(pluginid)

    def status(self) -> dict:
        """
        返回所有插件 id 及其对应的状态 ->
        {
            "absd1234edfaa11100": False,
            "...": True, ...
        }
        """
        result: Dict[str, Plugin] = dict()
        for id_, plugin in self.__plugins.items():
            result[id_] = plugin.status

        return result

    def start(self, pluginid: str) -> NoReturn:
        """
        尝试启动一个插件:
            plguinid: 要启动的插件 ID
        """
        # 尝试获取插件实例 - 当不存在时报错
        plugin: Plugin = self.__plugins.get(pluginid)
        if plugin is None:
            raise error.PluginNotFound(pluginid)

        # 如果插件的状态为已经启动 - 不进行操作
        if plugin.status is True:
            return

        # 尝试在新线程中运行插件的启动函数
        _start = Thread(target=plugin.start)
        _start.setDaemon(True)
        _start.start()
        plugin.status = True

    def unload(self, plguinid: str) -> NoReturn:
        """
        从注册表中删除一个插件的实例及信息
            pluginid: 插件的id
        """
        # 首先停止插件的运行
        self.stop(plguinid)

        # 从注册表中剔除
        plugin = self.__plugins.pop(plguinid, None)
        _catalog = self.__catalogs.pop(plguinid, None)
        module = self.__modules.pop(plugin, None)

        if plugin and module:
            del plugin
            del module

    def reload(self, pluginid: str) -> NoReturn:
        """
        从原来的目录位置重新载入模块和插件并重启:
            pluginid: 要操作的插件 ID
        *reload 之后的插件 id 将不会变化
        """
        # 首先停止插件
        self.stop(pluginid)

        # 重新载入模块
        module = self.__modules.get(pluginid)
        if not module:
            return
        newmodule = self.__reload(module)
        newplugin: Plugin = newmodule.plguin

        # 恢复插件原来的 id
        newplugin.id = pluginid

        # 更新内部的插件信息
        self.__modules[pluginid] = newmodule
        self.__plugins[pluginid] = newplugin

        # 启动插件
        newplugin.start()

    def stop(self, pluginid: str) -> NoReturn:
        """
        尝试停止一个插件:
            plguinid: 要启动的插件 ID
        """
        # 尝试获取插件实例 - 当不存在时报错
        plugin: Plugin = self.__plugins.get(pluginid)
        if plugin is None:
            raise error.PluginNotFound(pluginid)

        # 如果插件的状态为已经暂停 - 不进行操作
        if plugin.status is False:
            return

        # 尝试调用插件的停止函数
        plugin.stop()
        plugin.status = False

    def clean(self) -> NoReturn:
        """
        清理不存在的插件:
            从 self.__catalogs 中遍历目录
            当目录不在当前已知的目录中时判定插件已经删除
            对插件执行 stop + unload 操作
        """
        # 遍历目录
        catalogs: set = self.__scandirs(self.__directory, settings.skipped)
        exists: set = set(self.__catalogs.values())

        # 反转目录注册表用于查询插件id
        _reversed = {v: k for k, v in self.__catalogs.items()}

        # 检查是否有不存在的并删除
        for catalog in exists:
            if not catalog in catalogs:
                pluginid: str = _reversed.get(catalog)
                self.unload(pluginid)

    def scan(self, autorun: Optional[bool] = False) -> NoReturn:
        """
        尝试扫描指定的父目录并从中载入所有的插件:
            根据 settings.skipped 设定跳过扫描插件
        """

        # 载入目录后遍历查询 - 跳过已经载入的和不用载入的
        skipping: set = settings.skipped or set(self.__catalogs.values())
        catalogs: set = self.__scandirs(self.__directory, skipping)

        for catalog in catalogs:
            # 尝试载入插件 - 失败后放弃
            try:
                loaded = self.__load(catalog)
            except error.Error as _error:
                logger.error(_error)
                continue

            plugin: Plugin = loaded.plugin
            module: ModuleType = loaded.module

            # 保存信息
            self.__catalogs[plugin.id] = catalog
            self.__modules[plugin.id] = module
            self.__plugins[plugin.id] = plugin

            # 检测是否自动启动
            if autorun:
                self.start(plugin.id)

    def stopall(self) -> NoReturn:
        """
        停止所有函数
        用于在框架退出时执行所有插件的停止函数
        释放插件所使用的资源
        """
        for pluginid, _plugin in self.__plugins.items():
            self.stop(pluginid)

    def startall(self) -> NoReturn:
        """
        启动所有的插件
        使用 gunicorn 时使用 preload 模式预加载之后 startall
        """
        for pluginid, _plugin in self.__plugins.items():
            self.start(pluginid)
