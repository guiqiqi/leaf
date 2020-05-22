"""
注册插件事件
"""

from ...core import events

# 注册更新事件与停止事件
updated = events.Event("leaf.weixin.accesstoken.updated", ((str, int), {}), "Accesstoken 被更新")
failed = events.Event("leaf.weixin.accesstoken.failed", ((), {}), "Accesstoken 更新失败")
stopped = events.Event("leaf.weixin.accesstoken.stopped", ((), {}), "Accesstoken 插件停止运行")
