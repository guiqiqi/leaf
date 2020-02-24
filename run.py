"""框架运行示例文件"""

import logging
import flask

import leaf
import config

init = leaf.Init()
init.kernel()
init.logging(config.logging)
init.server()
init.database(config.database)

# 以下模块请根据需要启用/禁用初始化
init.plugins(config.plugins)  # 插件模块
init.weixin(config.weixin)  # 微信公众平台支持模块
init.wxpay(config.wxpay)  # 微信支付支持模块

# 获取服务模块
server: flask.Flask = leaf.modules.server

# 以下模块的获取根据您上面的启用情况以及需求进行
# plugins: leaf.plugins.Manager = leaf.modules.plugins  # 插件系统模块实例
# logger: logging.Logger = leaf.modules.logging.logger  # 日志系统模块实例
# events: leaf.core.events.Manager = leaf.modules.events  # 事件系统模块实例
# wxpay: leaf.core.algorithm.AttrDict = leaf.payments.wxpay  # 微信支付模块实例
# weixin: leaf.core.algorithm.AttrDict = leaf.modules.weixin  # 微信公众平台模块实例
# schedules: leaf.core.schedule.Manager = leaf.modules.schedules  # 任务调度模块实例

# 如果需要启用 Flask 自带的 Web Server 进行调试
# 请取消下面一行的注释并给定 Flask 运行参数即可
# server.run(host="0.0.0.0", port=80, ...)
