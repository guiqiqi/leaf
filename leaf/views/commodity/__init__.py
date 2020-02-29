"""关于商品与销售相关的视图函数"""

# pylint: disable=wrong-import-position

commodity = __import__("flask").Blueprint("commodity", __name__)

from . import product
from . import stock
