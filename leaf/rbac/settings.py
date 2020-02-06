"""用户, 组, 认证相关的设置文件"""


class User:
    """用户相关的设置文件"""
    # 是否允许同一种索引方式存在多个
    # 例如同账户绑定了多个不同的微信号
    # 默认情况不被允许
    AllowMultiAccountBinding = False

    class Index:
        """索引设置"""
        Id = ("1B4E705F3305F7FB", "通过用户ID索引")  # 通过用户id索引
        Mail = ("EAC366AD5FEA1B28", "通过邮件索引")  # 通过邮件索引
        Name = ("0C6B4A2B8AAEDDBC", "通过用户名索引")  # 通过用户名索引
        Phone = ("5E4BC1ABDDAACA4A", "通过手机号索引")  # 通过手机号索引


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
