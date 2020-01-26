"""订单类数据库模型"""

import mongoengine

from ..commodity import stock

class Order(mongoengine.Document):
    """
    订单类数据库模型:
        amount: 订单总金额 - float
        goods: 购买商品列表 - List[CacheedRef]
        status: 当前状态JSON字串 - str
        instance: 订单状态管理器的 pickle 对象 - bytes
    """
    amount = mongoengine.FloatField(min_value=0, required=True)
    goods = mongoengine.ListField(mongoengine.LazyReferenceField(stock.Stock))
    status = mongoengine.StringField(default=str)
    instance = mongoengine.BinaryField(default=bytes)
