"""Hello Leaf"""

import logging
import leaf
import flask
import config

# 初始化核心模块
init = leaf.Init()
init.kernel(config.basic)
init.logging(config.logging)
init.server(config.devlopment)
# init.database(config.database)

# 初始化插件与微信模块
init.weixin(config.weixin)  # 微信公众平台支持模块
init.plugins(config.plugins)  # 插件模块

# 获取模块实例
logger = logging.getLogger("leaf.demo.hello")
server: flask.Flask = leaf.modules.server  # 服务器模块
message: leaf.weixin.reply.Message = leaf.modules.weixin.message  # 微信公众平台消息处理模块实例

# 处理文本类型的消息
@message.register("text")
def reply_hello(**kwargs):
    """返回 Hello Leaf"""
    content = kwargs.get("content")
    logger.debug("MessageReceived: " + content)
    return leaf.weixin.reply.Maker.text("Hello Leaf!")

# 在主页也返回一个 Hello Leaf
@server.route("/")
def show_hello():
    """返回 Hello Leaf"""
    return "<h1>Hello Leaf!</h1>"

server.run(host="0.0.0.0", port=80)
