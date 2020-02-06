"""用户相关的数据库操作函数集合"""

from typing import List

import mongoengine
from bson import ObjectId

from . import error
from .. import settings
from ..model import User
from ..model import UserIndex


class Create:
    """创建用户静态函数集合"""


class Retrieve:
    """查询用户静态函数集合"""

    @staticmethod
    def byindex(typeid: str, value: str) -> List[User]:
        """通过 Index 用户索引文档查询用户记录"""
        # pylint: disable=no-member
        return User.objects(indexs__value=value,
                            indexs__typeid=typeid)

    @staticmethod
    def byid(userid: ObjectId) -> User:
        """通过用户 Id 查询用户文档"""
        # pylint: disable=no-member
        users = User.objects(id=userid)
        if not users:
            raise error.UserNotFound(str(userid))
        return users[0]

    @staticmethod
    def initialized(userid: ObjectId) -> bool:
        """查询用户是否被初始化"""
        user: User = Retrieve.byid(userid)
        if not user.indexs:
            return False
        return True


class Update:
    """更新用户静态函数集合"""

    @staticmethod
    def index(userid: ObjectId, userindex: UserIndex) -> User:
        """
        该函数将为用户新增一种索引类型:
            1. 首先会检查指定的索引值是否被其他用户绑定过
            2. 尝试插入检查是否发生 unique 错误
        """
        # 检查是否其他用户已经绑定过
        typeid, value = userindex.typeid, userindex.value
        if Retrieve.byindex(typeid, value):
            raise error.UserIndexValueBound(typeid + " - " + value)

        try:
            user: User = Retrieve.byid(userid)
            user.indexs.append(userindex)
        except mongoengine.NotUniqueError as _error:
            raise error.UserIndexTypeBound(typeid)
        else:
            return user.save()

    @staticmethod
    def inituser(userid: ObjectId) -> User:
        """
        该函数将为用户创建ID索引
        创建一个用户的接口调用顺序如下:
            1. 首先调用创建用户接口 - View 层处理
            2. 调用为用户设置密码接口 - auth.Create.withuserid
            3. 为用户设置文档ID索引 - 该接口
        """
        try:
            # pylint: disable=no-member
            user: User = Retrieve.byid(userid)

            # 为用户创建Id索引
            typeid, description = settings.User.Index.Id
            idindex = UserIndex(
                typeid=typeid, value=str(userid),
                description=description)
            user.indexs.append(idindex)

        except mongoengine.NotUniqueError as _error:
            raise error.UserInitialized(str(userid))
        except IndexError as _error:
            raise error.UserNotFound(str(userid))
        else:
            return user.save()


class Delete:
    """删除用户静态函数集合"""
