"""Leaf 框架配置示例文件"""


class Static(dict):
    """静态 Dict 类"""

    def __getattr__(self, key):
        """返回本地键值对"""
        return self[key]

    def __setattr__(self, key, value):
        """删除设置功能"""
        raise RuntimeError("StaticDict cannot be set value")

    def __delattr__(self, key):
        """删除删除功能"""
        raise RuntimeError("StaticDict cannot be remove value")


# 日志等级常量定义
CRITICAL, FATAL, ERROR = 50, 50, 40
WARNING, INFO, DEBUG, NOTSET = 30, 20, 10, 0

# 配置文件开始

# 错误与日志处理配置
logging = Static({
    "level": INFO,
    "rcfile": "leaf.log",
    "format": None,

    # 控制台输出配置
    "console": Static({
        "level": DEBUG,
        "format": None  # 表示使用父级 logger 配置
    }),

    # 文件输出配置
    "file": Static({
        "level": INFO,
        "format": None  # 表示使用父级 logger 配置
    })
})

# 微信公众平台配置
weixin = Static({
    "appid": "wxabcd1234abcd1234",
    "aeskey": "s5d6t7vybotcre3465d68f7ybvtd4sd5687g8huhyvt",
    "token": "s547d6figobunb67568d8f7g8ohjiks1"
})

# 微信支付配置
wxpay = Static({
    "appid": "wxabcd1234abcd1234",
    "mchid": "8888888888",
    "apikey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",

    # 回调地址
    "callbacks": {
        "pay": "https://xxx.com/wxpay/notify",
        "refund": "https://xxx.com/wxpay/notify_refund"
    },

    # 证书位置
    "cert": (
        "root\\key.pem",
        "root\\cert.pem"
    )
})

# 数据库配置
database = Static({
    "database": "test", # 需要连接的数据库
    "host": "localhost",  # 数据库服务器地址
    "port": 27017,  # 数据库服务端口
    "username": None,  # 数据库用户名 - None 表示不需要
    "password": None,  # 数据库密码 - None 表示不需要
    "timeout": 5  # 连接超时时间 - 秒为单位
})

# 插件配置
plugins = Static({
    "autorun": False,  # 插件是否自动运行
    "directory": None  # 是否从别处加载插件 - None 表示不需要
})
