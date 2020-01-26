"""插件运行的相关错误"""

# from .. import modules
# from ..core.error import Messenger
from ..core.error import Error


class PluginImportError(Error):
    """插件载入过程中出错"""
    code = 10101
    description = "插件载入时出错"


class PluginNotFound(Error):
    """无法根据给定的 ID 寻找到插件"""
    code = 10102
    description = "没有找到对应的插件"


class PluginInitError(Error):
    """不符合规范的插件"""
    code = 10103
    description = "插件 init 函数错误"


class PluginRuntimeError(Error):
    """插件运行期错误"""
    code = 10104
    description = "插件运行期间出现错误"
