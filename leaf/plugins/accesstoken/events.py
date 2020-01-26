"""
注册插件事件
"""

from ...core import events
from ...core import modules

# 注册更新事件与停止事件
updated = events.Event("leaf.plugins.accesstoken.updated", ((str, int), {}), "accesstoken 被更新")
stopped = events.Event("leaf.plugins.accesstoken.stopped", ((), {}), "accesstoken 插件停止运行")

emanager: events.Manager = modules.events
emanager.add(updated)
emanager.add(stopped)

# 设置插件停止通知后的插件停止状态
stopped.hook(lambda: modules.plugins.stop("a018e199e0624f29a06928865cfc9c7a"))
