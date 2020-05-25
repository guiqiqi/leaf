"""
使 leaf.weixin.accesstoken 模块获得的
微信公众平台 AccessToken 有接口对外公布
"""

from flask import abort

from ... import api
from ...core import modules
from ...weixin.accesstoken import Patcher
from ...core.abstract.plugin import Plugin

plugin = Plugin(
    "AccessToken 导出插件",
    Plugin.nothing, Plugin.nothing, Plugin.nothing,
    author="桂小方",
    description="将微信模块获取到的 AccessToken 对外公布",
    version="beta - 0.2.1",
    date="2020-05-23"
)

# 接口公开主机域
AuthorizedHost = ["127.0.0.1"]

# 注册插件主域
modules.plugins.register(plugin, ["accesstoken"])

# 导出接口
@plugin.route("/", methods=["GET"])
@api.wrapper.iplimit(AuthorizedHost)
@api.wrapper.wrap("accesstoken")
def accesstoken():
    """获取当前已经缓存的 accesstoken"""
    patcher: Patcher = modules.weixin.accesstoken
    return patcher.get()
