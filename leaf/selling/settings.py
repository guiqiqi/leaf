"""产品与销售相关设置"""

from ..core.schedule import HOUR

class Product:
    """产品相关的设置"""

    TagsCacheTime = 3 * HOUR  # 查询全部标签的缓存有效时间
