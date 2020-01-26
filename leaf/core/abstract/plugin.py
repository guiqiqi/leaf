"""Leaf 插件支持"""

import re
import uuid
from typing import NoReturn, Tuple, List, Dict, Callable, Optional

from flask import Response

from werkzeug.routing import Map, Rule, MapAdapter


class Plugin:
    """
    Leaf 插件类支持:
        route - 将插件中对应的试图函数返回
        before_request - 在请求之前执行的插件视图函数
        after_request - 在请求之后执行的插件视图函数
        id - 返回插件 id
        status - 返回/设置插件状态
        paras - 返回某插件需要的参数序列
        find - 返回在确定路径与方法下的插件视图函数
        info - 返回插件的信息
    """

    __pattern = re.compile("<.*?>")  # 搜索函数需要的参数序列

    @staticmethod
    def __nothing_did_func(*args, **kwargs) -> NoReturn:
        """一个什么都不干的函数"""

    @staticmethod
    def __id_generator() -> str:
        """返回 uuid1 生成的插件 id 值"""
        return uuid.uuid1().hex

    @staticmethod
    def __paras_finder(url: str) -> Tuple[str]:
        """
        根据传入的 url 在 werkzeug 标准中寻找参数序列
        *例如:
            "/admin/manage-<string:id>/<int:status>"
            -> ("id", "status")
        """
        # 首先在 url 中寻找所有的的 <> 标签
        paras = list()
        found = re.findall(Plugin.__pattern, url)

        # 之后根据 : 标签分割类型与名称
        for para in found:
            _ = para.split(':')[-1]
            paras.append(_.strip("<>"))

        return tuple(paras)

    @staticmethod
    def __paras_translator(kwargs: dict, paras: Tuple[str]) -> list:
        """
        根据 __paras_finder 的结果和获取到的 key-value 形式
        参数字典获取参数的详细列表形式
        *例如:
            {"id": "abcd1234", "status": 1}, ("id", "status")
            -> ["abcd1234", 1]
        *注意: 寻找不到的参数会用 None 代替
        """
        # 使用列表推导
        return [kwargs.get(key) for key in paras]

    def __hash__(self):
        """使插件实例支持 hash 函数"""
        return hash(self.__id)

    def __init__(self, name: str, start: Callable, reload: Callable,
                 stop: Callable, plugin_id: Optional[str] = None, **infomations):
        """
        插件类初始化函数
        start, reload, stop: 启动, 重载, 终止函数
        从 informations 中提取的信息有:
            author: 作者
            description: 描述
            version: 版本
            date: 更新时间
        """
        # 获取插件信息
        self.name = name
        self.start, self.reload, self.stop = start, reload, stop
        self.infomations = infomations

        # 运行标志位与服务名称
        self.__running = False
        self.__service_name = "leaf.plugins" + self.name

        # 请求前后绑定函数
        self.__func_before_request = self.__nothing_did_func
        self.__func_after_request = self.__nothing_did_func

        # 路由器的路由信息注册
        self.__urlmaps = Map()
        # endpoint 中视图函数与 para_tuple 注册表
        self.__para_views: Dict[Callable, tuple] = dict()
        # 路由转发器实例
        self.__adapter = self.__urlmaps.bind(self.__service_name)

        # 设置插件的运行 id
        if plugin_id is None:
            self.__id = self.__id_generator()
        else:
            self.__id = plugin_id

    def route(self, url: str, methods: Optional[List[str]] = None):
        """
        用来支持插件内部的视图函数路由:
            url: 要绑定视图函数的路由地址, 支持参数选择器,
            在绑定时可以使用 / 作为资源的分隔符, 但是在访问时会被替换成 .
            例如:
                @plugin.route("/admin/manage-<string:id>/<int:status>")
                def sth_very_interesting(id_: str, status: int) -> str:
                    ...
                访问时: plugin_name.admin.manage-id12345.0
            methods: 需要绑定的路由 HTTP 方法
            例如:
                ["GET", "POST", "HEAD", ...]
            当方法未找到时会触发 HTTP 405 错误

        *注意: 未指定 methods 参数时, 默认为 GET 方法
        """

        if methods is None:
            methods = ["GET"]

        def wrapper(function):
            """函数包装器"""
            # endpoint 设置成要调用的视图函数
            # 在 url 被调用时可以直接给出
            rule = Rule(url, methods=methods, endpoint=function)
            self.__urlmaps.add(rule)

            # 记录参数列表
            self.__para_views[function] = self.__paras_finder(url)

            # 更新转发器实例
            self.__adapter = self.__urlmaps.bind(self.__service_name)

        return wrapper

    def get_before_request(self) -> Callable:
        """获取 before_request 函数"""
        return self.__func_before_request

    def get_after_request(self) -> Callable:
        """获取 after_request 函数"""
        return self.__func_after_request

    def before_request(self, function: Callable):
        """在请求之前执行的函数(无参)"""
        self.__func_before_request = function

    def after_request(self, function: Callable[[Response], Response]):
        """在请求之后执行的函数(单独参数 - response)"""
        self.__func_after_request = function

    @property
    def id(self) -> str:
        """返回插件 id"""
        return self.__id

    @id.setter
    def id(self, newid: str) -> NoReturn:
        """给插件设置新的 id"""
        self.__id = newid

    @property
    def status(self) -> bool:
        """返回插件状态"""
        return self.__running

    @status.setter
    def status(self, new_status: bool) -> NoReturn:
        """设置新的插件状态"""
        self.__running = new_status

    def paramaters(self, endpoint: Callable) -> tuple:
        """返回插件所需要的参数列表"""
        return self.__para_views.get(endpoint, tuple())

    def find(self, url: str, method: str) -> Tuple[Callable, dict]:
        """查找方法和路径对应的视图处理函数"""
        adapter: MapAdapter = self.__adapter
        endpoint, paramaters = adapter.match(url, method=method)
        return endpoint, paramaters

    def info(self) -> dict:
        """返回插件信息"""
        return self.infomations
