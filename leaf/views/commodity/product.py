"""产品相关的视图函数"""

from typing import List, Dict
from flask import request

from . import commodity
from ...api import wrapper
from ...api import validator
from ...core.tools import web

# from ...selling.commodity import Stock
from ...selling.commodity import Product
# from ...selling.commodity import StocksGenerator
from ...selling.commodity import ProductParameter
from ...selling.functions import product as functions


@commodity.route("/products", methods=["GET"])
@wrapper.require("leaf.views.commodity.product.get")
@wrapper.wrap("products")
def get_batch_products() -> List[Product]:
    """批量获取产品信息"""

    # 获取页面参数
    previous: str = request.args.get(
        "previous", default='0' * 24, type=str)
    previous = validator.objectid(previous)
    count: int = request.args.get("count", default=0, type=int)

    # pylint: disable=no-member
    return Product.objects(id__gt=previous).limit(count)


@commodity.route("/products/<string:productid>", methods=["GET"])
@wrapper.require("leaf.views.commodity.product.get")
@wrapper.wrap("product")
def get_product_byid(productid: str) -> Product:
    """根据产品名称查找产品"""
    productid = validator.objectid(productid)
    return functions.Retrieve.byid(productid)


@commodity.route("/products/name/<string:name>", methods=["GET"])
@wrapper.require("leaf.views.commodity.product.get")
@wrapper.wrap("products")
def get_products_byname(name: str) -> List[Product]:
    """根据产品名查找全部相关的的产品"""
    return functions.Retrieve.byname(name)


@commodity.route("/products/tags/<string:tags>", methods=["GET"])
@wrapper.require("leaf.views.commodity.product.get")
@wrapper.wrap("products")
def get_products_bytags(tags: str) -> List[Product]:
    """根据产品标签查找产品 - 标签请根据 ‘,’ 分割"""
    tags = tags.split(',')
    return functions.Retrieve.bytags(tags)


@commodity.route("/products/tags", methods=["GET"])
@wrapper.require("leaf.views.commodity.product.get")
@wrapper.wrap("tags")
def get_all_tags() -> Dict[str, int]:
    """查询全部的标签以及个数"""
    return functions.Retrieve.tags()


@commodity.route("/products/<string:productid>", methods=["DELETE"])
@wrapper.require("leaf.views.commodity.product.delete")
@wrapper.wrap("status")
def delete_product(productid: str) -> bool:
    """删除一个指定的产品"""
    productid = validator.objectid(productid)
    product = functions.Retrieve.byid(productid)
    product.delete()
    return True


@commodity.route("/products/<string:productid>/parameters/<string:name>", methods=["DELETE"])
@wrapper.require("leaf.views.commodity.product.update")
@wrapper.wrap("parameters")
def delete_parameter_for_product(productid: str, name: str) -> List[ProductParameter]:
    """删除一个指定的产品参数"""
    productid = validator.objectid(productid)
    return functions.Delete.parameter(productid, name)


@commodity.route("/products/<string:productid>/parameters", methods=["POST"])
@wrapper.require("leaf.views.commodity.product.update")
@wrapper.wrap("parameters")
def add_parameter_for_product(productid: str) -> List[ProductParameter]:
    """增加一个产品参数"""
    name: str = request.form.get("name", default='', type=str)
    options: str = request.form.get("options", default="[]", type=str)
    options: List[str] = web.JSONparser(options)
    return functions.Create.parameter(productid, name, options)


@commodity.route("/products/<string:productid>/onsale", methods=["PUT"])
@wrapper.require("leaf.views.commodity.product.update")
@wrapper.wrap("product")
def update_product_status(productid: str) -> Product:
    """更新产品在售状态"""
    onsale: bool = request.form.get("onsale", default=True, type=bool)
    return functions.Update.onsale(productid, onsale)


@commodity.route("/products", methods=["POST"])
@wrapper.require("leaf.views.commodity.product.create")
@wrapper.wrap("product")
def create_product() -> Product:
    """创建一个产品"""
    name: str = request.form.get("name", default='', type=str)
    addition: str = request.form.get("addition", default='', type=str)
    description: str = request.form.get("description", default='', type=str)
    tags: str = request.form.get("tags", default="[]", type=str)
    tags: List[str] = web.JSONparser(tags)
    tags = [tag.strip().lower() for tag in tags]
    product = Product(name=name, addition=addition,
                      description=description, tags=tags)
    return product.save()
