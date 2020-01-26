"""商品数据模型"""

import mongoengine

from .product import Product


class Stock(mongoengine.Document):
    """
    商品数据模型:
        individual: 是否是独立的商品(非产品子类)
        attributes: 由产品生成时记录该商品的选项信息
        product: 父级产品类(当individual为False时)
        name: 商品名称(当individual为True时)
        describe: 商品描述(当individual为True时)
        addition: 商品附加信息(当individual为True时)
        tags: 商品标签列表(当individual为True时)
        price: 商品价格
        currency: 商品货币单位 ISO-4217
        inventory: 商品库存数量
        onsale: 商品是否上架
        extensions: 扩展数据存储
    """

    individual = mongoengine.BooleanField(required=True, default=False)
    product = mongoengine.ReferenceField(
        Product, reverse_delete_rule=mongoengine.CASCADE)
    name = mongoengine.StringField()
    attributes = mongoengine.DictField()
    describe = mongoengine.StringField()
    addition = mongoengine.StringField()
    tags = mongoengine.ListField(mongoengine.StringField())
    price = mongoengine.FloatField()
    currency = mongoengine.StringField()
    inventory = mongoengine.IntField()
    onsale = mongoengine.BooleanField()
    extensions = mongoengine.DictField(default=dict)
