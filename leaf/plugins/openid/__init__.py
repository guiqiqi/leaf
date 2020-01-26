"""
Leaf 微信公众平台前端获取 OpenID
"""

from . import error
from . import const
from . import settings

from ... import api
from ...core import modules
from ...core.tools import web
from ...core.abstract import plugin


def empty():
    """空函数"""


plugin = plugin.Plugin(
    "OpenID 获取器",
    empty, empty, empty,
    author="桂小方",
    description="提供OpenID获取功能",
    version="dev - 0.0.1",
    date="2019-09-26"
)

# 注册插件域
modules.plugins.register(plugin, ["openid"])


@plugin.route("/<string:code>", methods=["GET"])
@api.wrap("openid")
def openid(code: str) -> str:
    """获取 OpenID"""
    response, _ = web.get(const.address, {
        const.appid: settings.AppID,
        const.secret: settings.AppSecret,
        const.code: code,
        const.grant: const.default
    })

    response = web.JSONparser(response)
    if const.error in response:
        raise error.PatchError(response.get(const.errmsg, ''))

    return response.get(const.openid)
