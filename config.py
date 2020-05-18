"""Leaf 框架配置示例文件"""

# 以下是系统常量, 请勿进行修改

###############################################################

# 静态字典类


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

###############################################################

# 配置文件开始, 您可以开始您的配置

# 基础相关配置
# domain - 您部署 Leaf 的域名
# locker - 进程锁文件名 - 一般无需更改
# manager - 管理器连接地址 - 一般无需更改
# autkey - 管理器验证密钥 - 请更换成您喜欢的英文单词
basic = Static({
    "domain": "wxleaf.dev",
    "locker": ".leaf.lock",
    "manager": None,
    "authkey": "password"
})


# 开发相关配置
# 在生产环境请务必禁用开发者模式!
# enable: 启用开发者模式 - 仅当为 True 时以下选项生效
#         该选项同时影响 Flask 的默认 Debug 启动参数
# token: 开发用 JWT Token - 无需验证身份
devlopment = Static({
    "enable": False,
    "token": "here is a secret token"
})


# 错误与日志处理配置
logging = Static({

    # 默认的日志等级; 一般不需要修改
    "level": INFO,

    # 日志的存储位置及名称
    # 请确保程序有该处的读写权限
    "rcfile": "leaf.log",

    # 日志格式 - None 表示使用默认; 更多配置请参考
    # https://docs.python.org/3/library/logging.html
    "format": None,

    # 控制台日志输出配置
    # level - 单独设置控制台的输出等级
    # format - 单独设置控制台的输出格式; None 表示继承上面的格式
    "console": Static({
        "level": DEBUG,
        "format": None  # 表示使用父级 logger 配置
    }),

    # 文件日志输出配置
    # level - 单独设置文件的输出等级
    # format - 单独设置文件的输出格式; None 表示继承上面的格式
    "file": Static({
        "level": ERROR,
        "format": None  # 表示使用父级 logger 配置
    })
})


# 微信公众平台配置
# appid - 微信公众平台 AppId
# aeskey - 微信公众平台 AESKey
# token - 微信公众平台消息传递 Token
weixin = Static({
    "appid": "wxabcd1234abcd1234",
    "aeskey": "s5d6t7vybotcre3465d68f7ybvtd4sd5687g8huhyvt",
    "token": "s547d6figobunb67568d8f7g8ohjiks1"
})


# 微信支付配置
# appid - 微信支付关联的公众号 AppId
# mchid - 微信支付商户 Id
# apikey - 微信支付 API 密钥
wxpay = Static({
    "appid": "wxabcd1234abcd1234",
    "mchid": "8888888888",
    "apikey": "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx",

    # 回调地址
    # pay - 表示支付成功的回调地址
    # refund - 表示退款成功的回调地址
    # 除非您有其余服务部署在以下地址, 否则请不要修改
    "callbacks": {
        "pay": "https://" + basic.domain + "/wxpay/notify",
        "refund": "https://" + basic.domain + "/wxpay/notify_refund"
    },

    # 退款操作证书位置
    # 第一个为签名文件路径, 第二个为证书文件路径
    # 请填写绝对路径
    # 如果您确定自己的不需要使用退款功能, 可以随意填写
    "cert": (
        "root\\key.pem",
        "root\\cert.pem"
    )
})


# 数据库配置
# database - 需要连接的数据库
# host - 数据库服务器地址
# port - 数据库服务端口
# username - 用户名; None 表示不需要
# password - 密码; None 表示不需要
# timeout - 连接超时时间; 以秒为单位
database = Static({
    "database": "test",
    "host": "localhost",
    "port": 27017,
    "username": None,
    "password": None,
    "timeout": 5
})


# 插件配置
# autorun - Leaf 启动时插件是否自动运行
# directory - 插件加载位置; None 表示不需要
plugins = Static({
    "autorun": False,
    "directory": None
})
