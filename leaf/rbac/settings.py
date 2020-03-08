"""用户, 组, 认证相关的设置文件"""

from collections import namedtuple
from ..core.algorithm import StaticDict


Index = namedtuple("Index", ("typeid", "description"))


class User:
    """用户相关的设置文件"""
    # 是否允许同一种索引方式存在多个
    # 例如同账户绑定了多个不同的微信号
    # 默认情况不被允许
    # 选项被禁用 - 2020.2.19
    # AllowMultiAccountBinding = False

    # 头像与缩略图大小 - (width, height, 是否强制缩放)
    AvatarSize = (80, 80, True)
    AvatarThumbnailSize = (50, 50, True)
    AvatarType = {"jpg", "jpeg", "png", "gif"}

    Indexs = StaticDict({
        # 根据 Id 的索引方式请勿删除 - 会导致错误
        "Id": Index("1B4E705F3305F7FB", "通过用户ID索引"),  # 通过用户id索引

        # 下面的索引方式可以拓展
        "Mail": Index("EAC366AD5FEA1B28", "通过邮件索引"),  # 通过邮件索引
        "Name": Index("0C6B4A2B8AAEDDBC", "通过用户名索引"),  # 通过用户名索引
        "Phone": Index("5E4BC1ABDDAACA4A", "通过手机号索引")  # 通过手机号索引
    })


class Authentication:
    """认证相关的设置文件"""

    class Security:
        """安全策略设置"""
        SaltLength = 128  # 密钥盐的长度(bits)
        SaltCahce = 128  # 盐数据库查询的缓存数量
        PasswordHashCycle = 4  # 对密码进行迭代哈希的次数

    class Description:
        """描述字符串"""
        Id = "通过用户ID验证"
        Mail = "通过邮相验证"
        Name = "通过用户名验证"
        Phone = "通过电话验证"
