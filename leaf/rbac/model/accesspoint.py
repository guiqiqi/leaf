"""访问权限点的数据库模型建立"""

import mongoengine

from .user import User


class AccessPoint(mongoengine.Document):
    """
    权限访问点的数据库模型:
        pointname: 权限点名称(e.g. leaf.plugins.wxtoken.get)
        required: 需求的最小权限值
        strict: 是否要求仅仅指定权限值的用户可访问
        description: 当前权限点的描述
        exceptions: 针对某些用户的特例
    """

    pointname = mongoengine.StringField(primary_key=True)
    required = mongoengine.IntField(required=True)
    strict = mongoengine.BooleanField(default=False)
    description = mongoengine.StringField(default=str)
    exceptions = mongoengine.ListField(
        field=mongoengine.LazyReferenceField(User), default=list)
