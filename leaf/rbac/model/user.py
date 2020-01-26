"""用户数据模型"""

import mongoengine

from ..settings import User as settings
from ...core.tools import time

from . import Group


class UserIndex(mongoengine.EmbeddedDocument):
    """
    用户索引内嵌文档模型:
        typeid: 类型id 同一种索引方式相同
        value: 用户索引值
        description: 用户索引描述
        extension: 扩展描述字典
    """

    typeid = mongoengine.StringField(
        unique=not settings.AllowMultiAccountBinding, required=True)
    value = mongoengine.StringField(unique=True, required=True)
    description = mongoengine.StringField(default=str)
    extension = mongoengine.MapField(field=mongoengine.StringField())


class User(mongoengine.Document):
    """
    用户数据库模型:
        created: 创建时间 默认为utc时间
        disabled: 用户是否已被禁用
        groups: 用户被分配到的用户组信息
        indexs: 用户的索引信息列表
        informations: 用户的个人信息
    """

    created = mongoengine.IntField(default=time.now)
    disabled = mongoengine.BooleanField(default=False)
    groups = mongoengine.ListField(mongoengine.ReferenceField(
        Group, reverse_delete_rule=mongoengine.PULL), default=list)
    indexs = mongoengine.EmbeddedDocumentListField(UserIndex, default=list)
    informations = mongoengine.DictField()
