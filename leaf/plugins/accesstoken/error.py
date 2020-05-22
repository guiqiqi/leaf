"""AccessToken 导出插件错误定义"""

from ...core.error import Error as _Error


class PatcherNotRunning(_Error):
    """更新器不再运行"""
    code = 40101
    description = "AccessToken 更新器当前未在运行"
