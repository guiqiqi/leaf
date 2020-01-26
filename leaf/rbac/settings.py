"""用户, 组, 认证相关的设置文件"""

class User:
    """用户相关的设置文件"""
    # 是否允许同一种索引方式存在多个
    # 例如同账户绑定了多个不同的微信号
    # 默认情况不被允许
    AllowMultiAccountBinding = False

    class IndexId:
        """索引id设置"""
        Id = "1B4E705F3305F7FB" # 通过用户id索引
        Mail = "EAC366AD5FEA1B28" # 通过邮件索引
        Name = "0C6B4A2B8AAEDDBC" # 通过用户名索引
        Phone = "5E4BC1ABDDAACA4A" # 通过手机号索引
