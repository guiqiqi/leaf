"""
Leaf 微信公众平台AccessToken管理插件
"""

from flask import abort
from flask import request

from . import patch
from . import error
from . import events
from . import settings

from ... import api
from ...core import modules
from ...core.abstract import plugin

# 获取器实例
patcher = patch.Patcher(settings.AppID, settings.AppSecret)

plugin = plugin.Plugin(
    "AccessToken 中间控制插件",
    patcher.start, patcher.restart, patcher.stop,
    "a018e199e0624f29a06928865cfc9c7a",
    author="桂小方",
    description="提供一个微信公众平台 AccessToken 中控服务器",
    version="beta - 0.1.1",
    date="2019-09-09"
)

# 注册主域
modules.plugins.register(plugin, ["accesstoken"])


@plugin.route("/", methods=["POST"])
@api.wrapper.iplimit(["127.0.0.1"])
@api.wrapper.wrap("accesstoken")
def accesstoken():
    """获取当前已经缓存的 accesstoken"""
    return patcher.get()
