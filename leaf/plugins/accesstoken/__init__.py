"""
使 leaf.weixin.accesstoken 模块获得的
微信公众平台 AccessToken 有接口对外公布
"""

from flask import abort

from . import error
from . import settings

from ... import api
from ...core import modules
from ...weixin.accesstoken import Patcher
from ...core.abstract.plugin import Plugin

plugin = Plugin(
    "AccessToken 导出插件",
    Plugin.nothing, Plugin.nothing, Plugin.nothing,
    author="桂小方",
    description="将微信模块获取到的 AccessToken 对外公布",
    version="beta - 0.2.0",
    date="2020-05-23"
)

# 注册插件主域
modules.plugins.register(plugin, ["accesstoken"])

# 导出接口
@plugin.route("/", methods=["GET"])
@api.wrapper.iplimit(settings.AuthorizedHost)
@api.wrapper.wrap("accesstoken")
def accesstoken():
    """获取当前已经缓存的 accesstoken"""
    patcher: Patcher = modules.weixin.accesstoken

    # 如果更新器不在运行返回
    if not patcher.status:
        raise error.PatcherNotRunning()

    return patcher.get()
