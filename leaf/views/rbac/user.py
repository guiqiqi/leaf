"""用户视图函数"""

from typing import List

from flask import g
from flask import request
from bson import ObjectId

from . import rbac

from ...core import tools
from ...api import validator
from ...api import wrapper
from ...api import settings

from ...rbac import error
from ...rbac.model import User
from ...rbac.model import UserIndex
from ...rbac import settings as _rbac_settings
from ...rbac.functions import auth as authfuncs
from ...rbac.functions import user as functions


@rbac.route("/users", methods=["GET"])
@wrapper.require("leaf.views.rbac.user.batch")
@wrapper.wrap("users")
def get_batch_users() -> List[User]:
    """批量获取用户信息 - 暂时只能根据ID正向排序"""
    previous: ObjectId = request.args.get(
        "previous", default='0' * 24, type=ObjectId)
    count: int = request.args.get("count", default=0, type=int)
    # pylint: disable=no-member
    return User.objects(id__gt=previous).limit(count)


@rbac.route("/users/<string:userid>", methods=["GET"])
@wrapper.require("leaf.views.rbac.user.get")
@wrapper.wrap("user")
def get_user_byid(userid: str) -> User:
    """根据用户 ID 查询用户"""
    userid = validator.objectid(userid)
    return functions.Retrieve.byid(userid)


@rbac.route("/users/<string:indexid>/<string:index>", methods=["GET"])
@wrapper.require("leaf.views.rbac.user.query")
@wrapper.wrap("user")
def get_user_byindex(indexid: str, index: str) -> User:
    """根据用户 Index 查询用户"""
    users: [User] = functions.Retrieve.byindex(indexid, index)
    return users


@rbac.route("/users/<string:userid>/informations", methods=["PUT"])
@wrapper.require("leaf.views.rbac.user.update", byuser=True)
@wrapper.wrap("user")
def update_user_informations(userid: str) -> User:
    """更新用户 informations 信息"""

    # 检查是否由本人发起
    if userid != g.userid:
        return settings.Authorization.UnAuthorized(
            error.AuthenticationError(g.userid))

    user: User = functions.Retrieve.byid(userid)
    informations: dict = request.form.to_dict()
    user.informations = informations
    return user.save()


@rbac.route("/users", methods=["POST"])
@wrapper.require("leaf.views.rbac.user.create")
@wrapper.wrap("user")
def create_user() -> User:
    """
    创建一个用户的接口调用顺序如下:
        1. 首先调用创建用户接口 - User(**info...)
        2. 调用为用户设置密码接口 - auth.Create.withuserid
        3. 为用户设置文档ID索引 - user.Update.inituser
    这里密码应该通过 post 参数传入
    """
    status: bool = request.form.get("status", default=True, type=bool)
    password: str = request.form.get("password", default='', type=str)
    user: User = User(disabled=not status)
    user.save()
    # pylint: disable=no-member
    authfuncs.Create.withuserid(user.id, password)
    return functions.Update.inituser(user.id)


@rbac.route("/users/<string:userid>/status", methods=["PUT"])
@wrapper.require("leaf.views.rbac.user.update")
@wrapper.wrap("user")
def update_user_status(userid: str) -> User:
    """更新一个用户的状态"""
    status: bool = request.form.get("status", default=True, type=bool)
    user: User = functions.Retrieve.byid(userid)
    user.disabled = not status
    return user.save()


@rbac.route("/users/<string:userid>/indexs", methods=["POST"])
@wrapper.require("leaf.views.rbac.user.update", byuser=True)
@wrapper.wrap("user")
def update_user_index(userid: str) -> List[UserIndex]:
    """
    为指定用户增加一个索引信息
    请确保给定的索引方式在 rbac.settings.User.Index 中存在
    """

    # 检查是否由本人发起
    if userid != g.userid:
        return settings.Authorization.UnAuthorized(
            error.AuthenticationError(g.userid))

    indexs = dict(_rbac_settings.User.Indexs.values())

    typeid = request.form.get("typeid", type=str)
    value = request.form.get("value", type=str)
    extension = request.form.get("extension", type=str, default="{}")
    extension = tools.web.JSONparser(extension)
    if not typeid in indexs.keys():
        raise error.UndefinedUserIndex(typeid)

    description = indexs.get(typeid)
    index = UserIndex(typeid, value, description, extension)
    return functions.Create.index(userid, index)


@rbac.route("/users/<string:userid>/indexs/<string:typeid>", methods=["DELETE"])
@wrapper.require("leaf.views.rbac.user.update", byuser=True)
@wrapper.wrap("user")
def delete_user_index(userid: str, typeid: str) -> List[UserIndex]:
    """删除用户的一种指定索引"""

    # 检查是否由本人发起
    if userid != g.userid:
        return settings.Authorization.UnAuthorized(
            error.AuthenticationError(g.userid))

    return functions.Delete.index(userid, typeid)


@rbac.route("/users/<string:userid>", methods=["DELETE"])
@wrapper.require("leaf.views.rbac.user.delete", byuser=True)
@wrapper.wrap("status")
def delete_user(userid: str) -> bool:
    """删除某一个用户"""

    # 检查是否由本人发起
    if userid != g.userid:
        return settings.Authorization.UnAuthorized(
            error.AuthenticationError(g.userid))

    user: User = functions.Retrieve.byid(userid)
    user.delete()
    return True
