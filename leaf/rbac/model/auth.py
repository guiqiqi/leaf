"""认证记录数据库模型"""

import mongoengine

from . user import User


class Authentication(mongoengine.Document):
    """
    身份验证内嵌文档模型:
        user: 被建立登陆方式的用户id
        index: 用户索引(账户名-主键)
        salt: 用户密码盐
        token: 用户密码加盐之后的哈希值
        status: 验证方式是否可用
        description: 身份验证方式描述
    """

    index = mongoengine.StringField(primary_key=True)
    user = mongoengine.LazyReferenceField(
        User, reverse_delete_rule=mongoengine.CASCADE)
    salt = mongoengine.StringField(required=True)
    token = mongoengine.StringField(required=True)
    status = mongoengine.BooleanField(default=True)
    description = mongoengine.StringField(default=str)
