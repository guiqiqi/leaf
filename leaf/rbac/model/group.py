"""用户组数据库模型"""

import mongoengine


class Group(mongoengine.Document):
    """
    用户组模型:
        name: 用户组的名称
        description: 用户组的描述信息
        permission: 用户组的权限值
        users: 用户组中包含的用户
        extensions: 扩展信息存储
    """

    name = mongoengine.StringField(required=True, default=str)
    description = mongoengine.StringField(default=str)
    permission = mongoengine.IntField(required=True, default=int)
    users = mongoengine.ListField(mongoengine.ObjectIdField())
    extensions = mongoengine.MapField(field=mongoengine.StringField())
