"""商品相关的视图函数"""

from typing import List
from flask import request

from . import commodity
from ...api import wrapper
from ...api import validator
# from ...core.tools import web

from ...selling.commodity import Stock


@commodity.route("/goods", methods=["GET"])
@wrapper.require("leaf.views.commodity.product.get")
@wrapper.wrap("goods")
def query_individual_goods() -> List[Stock]:
    """查询所有的商品"""

    individual: bool = bool(request.args.get("individual", default=1, type=int))
    count: int = request.args.get("count", default=0, type=int)
    previous: str = request.args.get("previous", default='0' * 24, type=str)
    previous = validator.objectid(previous)

    # pylint: disable=no-member
    if individual:
        return list(Stock.objects(individual=True, id__gt=previous)).limit(count)
    return list(Stock.objects(id__gt=previous)).limit(count)


# @commodity.route("/goods", methods=["PUT"])
# @commodity.route("/goods", methods=["POST"])
# @commodity.route("/goods/<string: goodid>", methods=["GET"])
# @commodity.route("/goods/<string: goodid>", methods=["DELETE"])
