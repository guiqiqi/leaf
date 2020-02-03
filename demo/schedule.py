"""
Leaf 框架任务计划与事件回调功能演示:

这个 demo 演示了 Leaf 事件/任务计划功能的简单使用
自动获取wordpress文章更新并推送到微信公众号:
    1. 设置一个自定义事件 - 当发现文章更新时的动作
    2. 将给微信号推送文章绑定到这个自定义事件上
    3. 设置一个定时任务 - 每隔一个指定的事件就去获取一次wp的feed源
    4. 当发现更新时触发事件（即给公众号推送通知）

使用到的包有:
    1. leaf.core.web.get/post - 封装好的网络操作函数库
    2. leaf.core.web.XMLparser - 使用树算法封装的XML->dict库
    3. leaf.core.event - Leaf 事件类与管理器
    4. leaf.core.error - Leaf 错误与日志管理器
    5. leaf.weixin.templates - 公众平台文章推送封装

使用到的插件有:
    leaf.plugins.accesstoken - 微信公众平台 AccessToken 中控
"""

import logging
from typing import NoReturn

import leaf
import config

_ADDRESS = "https://init.blog/feed/"  # 订阅源地址
_ACTOKEN = "http://localhost/plugins/accesstoken"  # 获取 Token 地址
_GAP = leaf.core.schedule.HOUR * 3  # 每三个小时检查一次
_TEMPLATE_ID = "this is your template id"  # 推送消息模板ID
_LAST_COMMIT = dict()  # 最后一次的
_USERS = (
    "wx1234567812345678ab", "wx1234567812345678ab",
    "wx1234567812345678ab", "wx1234567812345678ab",
    "wx1234567812345678ab", "wx1234567812345678ab",
    ...
)


# 初始化 Leaf 框架 - 这里没有必要启用 wxpay 模块
init = leaf.Init()
init.kernel()
init.logging(config.logging)
init.server()
init.database(config.database)
init.weixin(config.weixin)
init.plugins(config.plugins)
logger = logging.getLogger("leaf.demo.schedule")


def make_data(_data: dict) -> dict:
    """制作推送消息的 dict - 自定义"""


def notify(data: dict) -> NoReturn:
    """向公众平台发起请求"""
    content, _response = leaf.core.tools.web.post(_ACTOKEN, {})
    accesstoken = leaf.core.tools.web.JSONparser(content).get("accesstoken")
    for user in _USERS:
        leaf.weixin.apis.template.send(
            accesstoken, user, _TEMPLATE_ID, make_data(data))


def update() -> NoReturn:
    """获取文章更新"""
    content, _response = leaf.core.tools.web.get(_ADDRESS)
    posts = leaf.core.tools.web.XMLparser(content)
    if posts != _LAST_COMMIT:
        newest = posts['rss']['channel']['item'][0]
        _LAST_COMMIT = posts
        updated.notify(newest)  # 通知事件调用函数


# 创建自定义事件并 Hook 动作
updated = leaf.core.events.Event(
    name="wordpress.post.updated", paras=((str), {}),
    description="Wordpress 文章更新了")
updated.hook(notify)

# 获取任务计划管理器并启动计划
schedules: leaf.core.schedule.Manager = leaf.modules.schedules
work = leaf.core.schedule.Worker(update, _GAP)
schedules.start(work)
leaf.modules.server.run()
