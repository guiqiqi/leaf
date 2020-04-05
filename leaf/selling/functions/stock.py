"""商品的相关CRUD函数"""

from typing import List
from bson import ObjectId

from .. import error
from ..commodity import Stock

class Retrieve:
    """查询相关函数"""

    @staticmethod
    def byid(goodid: ObjectId) -> Stock:
        """根据商品ID查询商品"""
        # pylint: disable=no-member
        goods: List[Stock] = Stock.objects(id=goodid)
        if not goods:
            raise error.StockNotFound(goodid)
        return goods[0]


class Delete:
    """删除相关函数"""


class Create:
    """创建相关函数"""


class Update:
    """更新相关函数"""
