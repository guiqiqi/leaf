"""对插件路由的支持"""

from typing import Iterable

from flask import g
from flask import abort
from flask import request
from flask import Response
from flask import Blueprint

from ..core import modules
from ..core.abstract.plugin import Plugin
from ..plugins import Manager

# 生成蓝图
plugins = Blueprint("plugins", __name__)

# 所有 HTTP 方法
__ALL_METHODS = [
    'GET', 'HEAD', 'POST', 'PUT',
    'DELETE', 'CONNECT', 'OPTIONS',
    'TRACE', 'PATCH'
]


def __para_converter(paras: dict, order: Iterable) -> tuple:
    """
    根据给定的参数字典和顺序列表返回有序参数序列:
        __para_converter({
            "second": 2, "first": 1
        }, ("first", "second"))

    *注意: 当参数在 paras 中未找到时会以 None 代替 - 而不是引发 KeyError
    """
    result = tuple(paras.get(key) for key in order)
    return result


# 定义插件的 after_request 函数支持
@plugins.after_request
def after_request(response: Response) -> Response:
    """
    执行在 forward 函数中获取到的插件 after_request 函数
    """
    if g.success:
        g.plugin_func_after_request(response)
    return response

# 定义插件的函数支持
@plugins.route("/<string:token>", methods=__ALL_METHODS)
def forward(token: str) -> object:
    """
    从给定的 Token 中寻找需要运行的插件
    并将当前的的控制流移交给对应插件
    获取到数据之后进行返回

    *访问的 url 示例:
        init.blog/plugins/accesstoken.get
    """

    g.success = False

    # 获取插件的访问主域以及 url
    domain, *urls = token.split(".")
    url: str = '/'.join(urls)

    # 当访问主页时经过上述处理会得到空字符串
    url = '/' if not url else url

    # 获取插件管理器根据 domain 寻找插件
    manager: Manager = modules.plugins
    plugin: Plugin = manager.domain(domain)
    if plugin is None:
        return abort(404)

    # 运行插件的 before_request 函数并设置 after_request
    plugin.get_before_request()()
    g.success = True
    g.plugin_func_after_request = plugin.get_after_request()

    # 获取视图函数以及其需要的参数
    handler, paramaters = plugin.find(url, request.method)
    order = plugin.paramaters(handler)
    paramaters = __para_converter(paramaters, order)

    # 将控制流交给插件
    return handler(*paramaters)
