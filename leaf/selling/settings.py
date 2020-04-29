"""产品与销售相关设置"""

from ..core.schedule import HOUR


class General:
    """与交易相关的全局设置"""

    DefaultCurrency = "CNY"  # 默认的货币类型
    AllowCurrency = {
        "CNY", "USD", "RUB"
    }  # 允许设置的价格单位


class Product:
    """产品相关的设置"""

    TagsCacheTime = 3 * HOUR  # 查询全部标签的缓存有效时间
