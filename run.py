"""框架运行示例文件"""

import logging
import flask

import leaf
import config

# leaf.Master.connect()

init = leaf.Init()
leaf.init.kernel()
leaf.init.logging(config.logging)
leaf.init.server()
leaf.init.database(config.database)
leaf.init.plugins(config.plugins)
leaf.init.weixin(config.weixin)
leaf.init.wxpay(config.wxpay)

# 获取服务模块
server: flask.Flask = leaf.modules.server
plugins: leaf.plugins.Manager = leaf.modules.plugins
logger: logging.Logger = leaf.modules.logging.logger
events: leaf.core.events.Manager = leaf.modules.events
wxpay: leaf.core.algorithm.AttrDict = leaf.payments.wxpay
weixin: leaf.core.algorithm.AttrDict = leaf.modules.weixin
schedules: leaf.core.schedule.Manager = leaf.modules.schedules
database: leaf.core.database.MongoDBPool = leaf.modules.database

# __import__("pdb").set_trace()
server.run()
