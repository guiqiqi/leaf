"""
Leaf 框架初始化文件:
    api - API 支持
    core - 核心模块
    plugins - 插件模块
    payments - 支付模块
    modules - 运行时实例保存器

    init - 框架初始化函数
"""

import os as _os
import time as _time
import atexit as _atexit
from typing import Tuple as _Tuple
from typing import Union as _Union
from typing import Optional as _Optional
from typing import NoReturn as _NoReturn

import pymongo as _pymongo
import mongoengine as _mongoengine
from flask import Flask as _Flask

from . import api
from . import core
from . import rbac
from . import weixin
from . import selling
from . import plugins
from . import payments


modules = core.modules


class Init:
    """
    初始化 Leaf 框架资源的函数:
        kernel - 核心部分初始化函数 (第一个运行&仅一次)
        server - 服务器部分初始化函数
        logging - 覆盖错误与日志记录相关设置
        plugins - 插件部分的初始化函数
        weixin - 微信模块初始化函数
        wxpay - 微信支付模块初始化函数
        database - 连接池服务初始化函数
    """

    def __init__(self, _modules: _Optional[core.algorithm.AttrDict] = None):
        """
        初始化模块初始化函数:
            locker: 进程锁文件名
            address: 管理器地址
            authkey: 管理器连接密钥

            self.__modules - core.modules 核心动态模块
            self.__kernel_initialized - 核心是否被初始化过
            self.__modules.is_master - 进程是否为主进程
        """
        if _modules is None:
            _modules = modules

        # 给全局 modules 赋值
        core.modules = _modules

        # 核心初始化
        self.__modules = _modules
        self.__kernel_initialized = False

        # 是否有其他的 leaf 进程正在运行
        self.__modules.is_master = True

    def kernel(self, conf: core.algorithm.StaticDict) -> _NoReturn:
        """
        初始化:
            生成事件管理器
            生成任务计划调度模块
            注册核心模块 Events 中的错误信息
            添加退出 atexit 事件项目
        """
        if self.__kernel_initialized:
            return

        # 并行检测支持
        async_events = None  # 默认的事件同步队列为 None
        try:
            detector = core.parallel.Detector(conf.locker)
            self.__modules.is_master = detector.master
            handler = detector.locker
        except EnvironmentError as _error:
            import warnings as _w
            _w.warn("Communication with other Leaf processes failed.")
        else:

            # 如果工作在主模式 - 启用调度服务
            if detector.master:
                controller = core.parallel.Controller(
                    conf.manager, conf.authkey)
                address = controller.start()
                handler.write(str(address))
                handler.flush()

            # 获取调度服务地址 - 增加延迟保证主服务进程顺利写入地址
            _time.sleep(0.5)
            handler = open(conf.locker, 'r')
            address = handler.read().strip()
            handler.close()

            # 连接到调度服务
            manager = core.parallel.Controller.connect(address, conf.authkey)
            # pylint: disable=no-member
            async_events = manager.bind(_os.getpid())
            self.__modules.manager = manager

        # 保存错误日志的基础信息 - 默认配置
        self.__modules.error = core.algorithm.AttrDict()
        self.__modules.error.messenger = core.error.Messenger()

        # 利用反射自动搜索注册所有的错误子类信息
        errors = core.error.Error.__subclasses__()
        for instance in errors:
            self.__modules.error.messenger.register(instance)

        # 生成事件管理器与任务计划调度
        self.__modules.events = core.events.Manager(asyncs=async_events)
        self.__modules.schedules = core.schedule.Manager(
            not self.__modules.is_master)

        # 添加 leaf.exit 事件项目
        atexit = core.events.Event("leaf.exit", ((), {}), "在 Leaf 框架退出时执行")
        self.__modules.events.add(atexit)

        # 在 atexit 中注册退出函数
        _atexit.register(self.__modules.events.event("leaf.exit").notify)
        self.__kernel_initialized = True

    def plugins(self, conf: core.algorithm.StaticDict) -> plugins.Manager:
        """
        插件部分初始化:
            生成插件管理器
            注册初始化部分的错误信息
            扫描所有的插件目录并尝试载入
            注册插件蓝图
            注册框架退出事件时的所有插件清理函数
        """

        # 生成插件管理器
        if conf.directory is None:
            self.__modules.plugins = plugins.Manager(plugins.current)
        else:
            self.__modules.plugins = plugins.Manager(conf.directory)

        # 扫描所有并载入模块
        manager: plugins.Manager = self.__modules.plugins
        manager.scan(conf.autorun)

        # 注册插件蓝图
        server: _Flask = self.__modules.server
        from .views.plugins import plugins as _plugins
        server.register_blueprint(_plugins, url_prefix="/plugins")

        # 注册所有插件停止函数
        exiting: core.events.Event = self.__modules.events.event("leaf.exit")
        exiting.hook(self.__modules.plugins.stopall)

        return manager

    def wxpay(self, conf: core.algorithm.StaticDict) -> payments.wxpay.payment:
        """
        微信支付模块初始化:
            初始化支付模块
            注册微信支付蓝图
        """
        wxpay = payments.wxpay
        self.__modules.payments = core.algorithm.AttrDict()
        self.__modules.payments.wxpay = core.algorithm.AttrDict()

        # 初始化支付实例
        jsapi = payments.wxpay.payment(
            conf.appid, conf.mchid, conf.apikey,
            conf.callbacks, conf.cert, wxpay.methods.jsapi)
        native = payments.wxpay.payment(
            conf.appid, conf.mchid, conf.apikey,
            conf.callbacks, conf.cert, wxpay.methods.native)
        inapp = payments.wxpay.payment(
            conf.appid, conf.mchid, conf.apikey,
            conf.callbacks, conf.cert, wxpay.methods.inapp)

        self.__modules.payments.wxpay.jsapi = jsapi
        self.__modules.payments.wxpay.native = native
        self.__modules.payments.wxpay.inapp = inapp

        # 初始化加密实例
        signature = wxpay.signature(conf.apikey)
        self.__modules.payments.wxpay.signature = signature

        # 注册蓝图
        server: _Flask = self.__modules.server
        from .views.wxpay import wxpay as _wxpay
        server.register_blueprint(_wxpay, url_prefix="/wxpay")

        return jsapi

    def weixin(self, conf: core.algorithm.StaticDict) -> weixin.reply.Message:
        """
        微信模块初始化:
            生成微信加密套件
            注册微信加密套件
            注册微信消息套件
            注册微信蓝图
        """
        # 微信加密套件
        encryptor = weixin.Encrypt(conf.aeskey, conf.appid, conf.token)
        self.__modules.weixin = core.algorithm.AttrDict()
        self.__modules.weixin.encrypt = encryptor

        # 微信回复套件
        message = weixin.reply.Message(encryptor)
        event = weixin.reply.Event(encryptor)
        self.__modules.weixin.message = message
        self.__modules.weixin.event = event
        self.__modules.weixin.accesstoken = weixin.accesstoken.Patcher(
            conf.appid, conf.secret)

        # 判断是否启用 AccessToken 自动更新功能 - 仅在主进程启用
        if conf.accesstoken.enable:
            weixin.accesstoken.settings.MaxRetries = conf.accesstoken.retries
            if self.__modules.is_master:
                self.__modules.weixin.accesstoken.start()
        _events: core.events.Manager = self.__modules.events
        _events.add(weixin.accesstoken.events.updated)
        _events.add(weixin.accesstoken.events.failed)
        _events.add(weixin.accesstoken.events.stopped)

        # 设置在其他进程的 AccessToken 的更新事件
        weixin.accesstoken.events.updated.hook(
            self.__modules.weixin.accesstoken.set)

        # 注册微信公众平台错误码描述文件
        messenger: core.error.Messenger = self.__modules.error.messenger
        with open(weixin.settings.ErrcodesFile, 'r', encoding="utf-8") as handler:
            messenger.load(handler)

        # 注册微信蓝图
        from .views.weixin import weixin as _weixin
        server: _Flask = self.__modules.server
        server.register_blueprint(_weixin, url_prefix="/weixin")
        self.__modules.weixin.handler = _weixin

        return message

    def server(self, dev: core.algorithm.StaticDict) -> _Flask:
        """
        服务器初始化函数:
            创建 Flask 服务器
            替换 Flask 默认 logger
            设置服务器密钥
        """
        # 生成 Flask 应用服务器
        self.__modules.server = _Flask("leaf")
        self.__modules.server.logger = self.__modules.logging.logger
        self.__modules.server.secret_key = core.tools.encrypt.random(64)
        self.__modules.server.debug = dev.enable
        self.__modules.server.devjwt = dev.token

        # 引用其他的 views 视图函数并注册 Blueprints 蓝图
        server: _Flask = self.__modules.server
        from .views.rbac import rbac as _rbac
        from .views.commodity import commodity as _commodity
        from .views.order import order as _order
        server.register_blueprint(_rbac, url_prefix="/rbac")
        server.register_blueprint(_commodity, url_prefix="/commodity")
        server.register_blueprint(_order, url_prefix="/order")

        return self.__modules.server

    def database(self, conf: core.algorithm.StaticDict) -> _pymongo.MongoClient:
        """
        数据库连接池初始化函数
            初始化数据库连接池
            设置退出时关闭连接池
            设置数据库信息
        """
        # 取消数据库池的使用
        # pool = core.database.MongoDBPool(
        #     conf.size, conf.server, conf.port,
        #     conf.username, conf.password, conf.timeout)
        # self.__modules.database = pool

        client = _mongoengine.connect(db=conf.database, host=conf.host, port=conf.port,
                                      username=conf.username, password=conf.password,
                                      connectTimeoutMS=conf.timeout * 1000)

        exiting: core.events.Event = self.__modules.events.event("leaf.exit")
        exiting.hook(_mongoengine.disconnect)

        return client

    def logging(self, conf: core.algorithm.StaticDict) -> core.error.Logging:
        """
        当提供了配置信息时 - 重写错误日志的部分信息:
            logging.logger.formatter
            logging.file_handler
            logging.file_handler.level
            logging.console_handler.level
        """
        # 重新生成 Logger 实例
        if not conf.format is None:
            logging = self.__modules.logging = core.error.Logging(
                file=conf.rcfile, fmt=conf.format)
        else:
            logging = self.__modules.logging = core.error.Logging(
                file=conf.rcfile)

        # 配置文件记录
        file_handler = self.__modules.logging.file_handler
        file_handler.setLevel(conf.file.level)
        if not conf.file.format is None:
            file_handler.setFormatter(conf.file.format)

        # 配置 Console 记录
        console_handler = self.__modules.logging.console_handler
        console_handler.setLevel(conf.console.level)
        if not conf.console.format is None:
            console_handler.setFormatter(conf.console.format)

        # 设置全局日志级别
        self.__modules.logging.logger.setLevel(conf.level)

        # 尝试给 server 服务器更换 logger
        try:
            self.__modules.server.logger = self.__modules.logging.logger
        except KeyError as _error:
            pass

        return logging
