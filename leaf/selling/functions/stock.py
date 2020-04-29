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

    @staticmethod
    def byname(name: str, individual: bool = False) -> List[Stock]:
        """根据名称查找商品"""
        # pylint: disable=no-member
        if individual:
            return Stock.objects(name__icontains=name, individual=True)
        return Stock.objects(name__icontains=name)

    @staticmethod
    def bytags(tags: List[str], individual: bool = False) -> List[Stock]:
        """根据标签查找商品"""
        # 首先对标签进行头尾空格处理, 小写化处理
        tags = [tag.strip().lower() for tag in tags]

        #pylint: disable=no-member
        if individual:
            queryset: List[Stock] = Stock.objects(tags=tags[0], individual=True)
        else:
            queryset: List[Stock] = Stock.objects(tags=tags[0])

        for tag in tags[1::]:
            queryset = queryset.filter(tags=tag)
        return queryset


class Delete:
    """删除相关函数"""


class Create:
    """创建相关函数"""


class Update:
    """更新相关函数"""

    @staticmethod
    def onsale(goodid: str, status: bool) -> Stock:
        """更新商品在售信息"""
        good = Retrieve.byid(goodid)
        good.onsale = status
        return good.save()
