"""产品类型数据库模型"""

import mongoengine


class ProductParameter(mongoengine.EmbeddedDocument):
    """
    产品参数内嵌文档:
        name: 选项名称
        options: 可选项值列表
    """

    name = mongoengine.StringField()
    options = mongoengine.ListField()


class Product(mongoengine.Document):
    """
    产品类数据模型:
        name: 产品名称
        description: 产品描述
        addtion: 产品额外描述
        tags: 产品标签列表
        onsale: 产品是否上架
        parameters: 产品可选项目列表
        extension: 扩展数据存储
    """

    name = mongoengine.StringField()
    description = mongoengine.StringField()
    addition = mongoengine.StringField()
    tags = mongoengine.ListField(field=mongoengine.StringField())
    parameters = mongoengine.EmbeddedDocumentListField(ProductParameter)
    onsale = mongoengine.BooleanField(default=True)
    extensions = mongoengine.DictField(default=dict)
