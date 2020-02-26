"""产品相关的 RBAC 函数"""

from typing import List, Dict
from collections import defaultdict

import cacheout
import mongoengine
from bson import ObjectId

from .. import error
from .. import settings
from ..commodity import Product
from ..commodity import ProductParameter


class Create:
    """Product 创建类"""

    @staticmethod
    def parameter(productid: ObjectId, name: str,
                  options: List[str]) -> List[ProductParameter]:
        """给产品增加一个参数选项"""
        product = Retrieve.byid(productid)
        parameter = ProductParameter(name=name, options=options)

        try:
            product.parameters.get(name=name)
        except mongoengine.errors.DoesNotExist as _error:
            product.parameters.append(parameter)
        else:
            raise error.ProductParameterConflicting(name)

        return product.parameters.save()


class Update:
    """产品信息更新类"""

    @staticmethod
    def onsale(productid: ObjectId, status: bool) -> Product:
        """更新产品在售信息"""
        product = Retrieve.byid(productid)
        product.onsale = status
        return product.save()


class Retrieve:
    """Product 信息查询类"""

    tags_cache = cacheout.Cache(ttl=settings.Product.TagsCacheTime)

    @staticmethod
    def byid(productid: ObjectId) -> Product:
        """根据产品 Id 查询产品"""
        # pylint: disable=no-member
        product: List[Product] = Product.objects(id=productid)
        if not product:
            raise error.ProductNotFound(productid)
        return product[0]

    @staticmethod
    def byname(name: str) -> List[Product]:
        """根据名称查找产品"""
        # pylint: disable=no-member
        return Product.objects(name__icontains=name)

    @staticmethod
    def bytags(tags: List[str]) -> List[Product]:
        """根据产品标签查找产品"""
        # 首先对标签进行头尾空格处理, 小写化处理
        tags = [tag.strip().lower() for tag in tags]

        #pylint: disable=no-member
        queryset: List[Product] = Product.objects(tags=tags[0])
        for tag in tags[1::]:
            queryset = queryset.filter(tags=tag)
        return queryset

    @staticmethod
    @tags_cache.memoize()
    def tags() -> Dict[str, int]:
        """查询全部的 Tags"""
        tags = defaultdict(int)
        # pylint: disable=no-member
        for product in Product.objects:
            for tag in product.tags:
                tags[tag] += 1

        return tags


class Delete:
    """删除相关操作函数集合"""

    @staticmethod
    def parameter(productid: ObjectId, name: str) -> List[ProductParameter]:
        """删除产品的的一个指定参数"""
        product = Retrieve.byid(productid)
        try:
            parameter: ProductParameter = product.parameters.get(name=name)
        except mongoengine.errors.DoesNotExist as _error:
            raise error.ProductParameterNotFound(name)

        product.parameters.remove(parameter)
        return product.parameters.save()
