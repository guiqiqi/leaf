"""用户相关的数据库操作函数集合"""

from typing import List, NoReturn

import mongoengine
from bson import ObjectId

from . import auth
from . import group
from .. import error
from .. import settings
from ..model import User
from ..model import UserIndex


class Create:
    """创建用户静态函数集合"""

    @staticmethod
    def index(userid: ObjectId, userindex: UserIndex) -> List[UserIndex]:
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
            user.indexs.save()
            return user.indexs

    @staticmethod
    def group(userid: ObjectId, groupid: ObjectId) -> User:
        """
        向组中添加用户:
            向用户组的用户记录中添加
            向用户的组记录中添加
        """
        userid = ObjectId(userid)
        groupid = ObjectId(groupid)
        user = Retrieve.byid(userid)
        ugroup = group.Retrieve.byid(groupid)
        if not ugroup in user.groups:
            user.groups.append(ugroup)

        if not userid in ugroup.users:
            ugroup.users.append(userid)
        ugroup.save()

        return user.save()


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
    def inituser(userid: ObjectId) -> User:
        """
        该函数将为用户创建ID索引
        创建一个用户的接口调用顺序如下:
            1. 首先调用创建用户接口 - View 层处理
            2. 调用为用户设置密码接口 - auth.Create.withuserid
            3. 为用户设置文档ID索引 - 该接口
        """
        try:
            user: User = Retrieve.byid(userid)

            # 为用户创建Id索引
            typeid, description = settings.User.Indexs.Id
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

    @staticmethod
    def index(userid: ObjectId, typeid: str) -> NoReturn:
        """
        删除用户的某一种 Index
        同时要删除该 Index 对应的 Auth 文档
        """

        user: User = Retrieve.byid(userid)
        try:
            index = user.indexs.get(typeid=typeid)
        except mongoengine.errors.DoesNotExist as _error:
            return user.indexs

        user.indexs.remove(index)
        user.indexs.save()

        # 查找并删除指定的 Auth 文档
        # pylint: disable=no-member
        try:
            authdoc = auth.Retrieve.byindex(index.value)
        except error.AuthenticationNotFound as _error:
            pass
        else:
            authdoc.delete()

        return user.indexs

    @staticmethod
    def group(userid: ObjectId, groupid: ObjectId) -> NoReturn:
        """
        将用户从某个用户组中移除:
            将用户从用户组中移除
            将组中的用户记录删除
        """
        userid = ObjectId(userid)
        groupid = ObjectId(groupid)
        user = Retrieve.byid(userid)
        ugroup = group.Retrieve.byid(groupid)
        if ugroup in user.groups:
            user.groups.remove(ugroup)
        user.save()

        if userid in ugroup.users:
            ugroup.users.remove(userid)
        ugroup.save()
