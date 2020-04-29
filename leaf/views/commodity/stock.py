"""商品相关的视图函数"""

from typing import List
from flask import request

from . import commodity
from ...core.tools import web
from ...api import wrapper
from ...api import validator
from ...selling import error
from ...selling import settings
from ...selling.functions import stock as functions

from ...selling.commodity import Stock


@commodity.route("/goods", methods=["GET"])
@wrapper.require("leaf.views.commodity.product.get")
@wrapper.wrap("goods")
def query_individual_goods() -> List[Stock]:
    """查询所有的独立商品"""
    individual: bool = bool(request.args.get(
        "individual", default=1, type=int))
    count: int = request.args.get("count", default=0, type=int)
    previous: str = request.args.get("previous", default='0' * 24, type=str)
    previous = validator.objectid(previous)

    # pylint: disable=no-member
    if individual:
        return list(Stock.objects(individual=True, id__gt=previous)).limit(count)
    return list(Stock.objects(id__gt=previous)).limit(count)


@commodity.route("/goods/tags/<string:tags>", methods=["GET"])
@wrapper.require("leaf.views.commodity.product.get")
@wrapper.wrap("goods")
def query_individual_goods_bytags(tags: str) -> List[Stock]:
    """根据标签查询所有的独立商品 - 以 ',' 分割"""
    tags: List[str] = tags.split(',')
    return functions.Retrieve.bytags(tags, individual=True)


@commodity.route("/goods/name/<string:name>", methods=["GET"])
@wrapper.require("leaf.views.commodity.product.get")
@wrapper.wrap("goods")
def query_individual_goods_byname(name: str) -> List[Stock]:
    """根据名称查询所有的独立商品"""
    return functions.Retrieve.byname(name, individual=True)


@commodity.route("/goods/<string:goodid>", methods=["PUT"])
@wrapper.require("leaf.views.commodity.product.update")
@wrapper.wrap("good")
def update_specific_good(goodid: str) -> Stock:
    """更新一个特定的产品信息"""
    goodid = validator.objectid(goodid)
    good = functions.Retrieve.byid(goodid)
    good.name: str = request.form.get("name", default='', type=str)
    good.description: str = request.form.get(
        "description", default='', type=str)
    good.addition: str = request.form.get("addition", default='', type=str)
    good.price: float = request.form.get("price", default=0.00, type=float)
    currency: str = request.form.get(
        "currency", default=settings.General.DefaultCurrency, type=str)

    # 检查货币类型是否允许
    if not currency in settings.General.AllowCurrency:
        raise error.InvalidCurrency(currency)

    good.currency = currency
    good.inventory: int = request.form.get("inventory", default=0, type=int)
    return good.save()


@commodity.route("/goods", methods=["POST"])
@wrapper.require("leaf.views.commodity.product.create")
@wrapper.wrap("good")
def create_good_individually() -> Stock:
    """
    创建一个独立商品
    这里不设置 tags, extensions - 留作单独 API 接口设置
    """
    name: str = request.form.get("name", default='', type=str)
    product = validator.objectid('0' * 24)
    description: str = request.form.get("description", default='', type=str)
    addition: str = request.form.get("addition", default='', type=str)
    price: float = request.form.get("price", default=0.00, type=float)
    currency: str = request.form.get(
        "currency", default=settings.General.DefaultCurrency, type=str)

    # 检查货币类型是否允许
    if not currency in settings.General.AllowCurrency:
        raise error.InvalidCurrency(currency)

    inventory: int = request.form.get("inventory", default=0, type=int)
    stock = Stock(individual=True, product=product, name=name,
                  attributes=dict(), description=description,
                  addition=addition, tags=list(), price=price,
                  currency=currency, inventory=inventory, onsale=True)
    return stock.save()


@commodity.route("/goods/<string:goodid>/tags", methods=["PUT"])
@wrapper.require("leaf.views.commodity.product.update")
@wrapper.wrap("good")
def update_good_tags(goodid: str) -> Stock:
    """更改商品标签"""
    goodid = validator.objectid(goodid)
    good = functions.Retrieve.byid(goodid)
    tags: str = request.form.get("tags", default="[]", type=str)
    tags: List[str] = web.JSONparser(tags)
    good.tags = [tag.strip().lower() for tag in tags]
    return good.save()


@commodity.route("/goods/<string:goodid>/onsale", methods=["PUT"])
@wrapper.require("leaf.views.commodity.product.update")
@wrapper.wrap("good")
def update_good_status(goodid: str) -> Stock:
    """更新商品在售状态"""
    goodid = validator.objectid(goodid)
    onsale: bool = bool(request.form.get("onsale", default=1, type=int()))
    return functions.Update.onsale(goodid, onsale)


@commodity.route("/goods/<string:goodid>", methods=["GET"])
@wrapper.require("leaf.views.commodity.product.get")
@wrapper.wrap("good")
def query_specific_good(goodid: str) -> Stock:
    """查询一个指定的商品信息"""
    goodid = validator.objectid(goodid)
    return functions.Retrieve.byid(goodid)


@commodity.route("/goods/<string:goodid>", methods=["DELETE"])
@wrapper.require("leaf.views.commodity.product.delete")
@wrapper.wrap("result")
def delete_one_good(goodid: str) -> bool:
    """删除一个指定的商品"""
    goodid = validator.objectid(goodid)
    good = functions.Retrieve.byid(goodid)
    good.delete()
    return True
