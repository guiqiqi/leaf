"""用户视图函数"""

from typing import List
from flask import request
from bson import ObjectId
from . import rbac

from ...api import wrapper
from ...rbac.model import User
# from ...rbac.model import Group
# from ...rbac.model import UserIndex
# from ...rbac.model import Authentication
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
    return functions.Retrieve.byid(userid)


@rbac.route("/users/<string:indexid>/<string:index>", methods=["GET"])
@wrapper.require("leaf.views.rbac.user.query")
@wrapper.wrap("user")
def get_user_byindex(indexid: str, index: str) -> User:
    """根据用户 Index 查询用户"""
    return functions.Retrieve.byindex(indexid, index)


@rbac.route("/users/<string:userid>/informations", methods=["PUT"])
@wrapper.require("leaf.views.rbac.user.update")
@wrapper.wrap("user")
def update_user_informations(userid: str) -> User:
    """更新用户 informations 信息"""
    user: User = functions.Retrieve.byid(userid)
    informations: dict = request.form.to_dict()
    user.informations = informations
    return user.save()


# @rbac.route("/users", methods=["POST"])
# @wrapper.require("leaf.views.rbac.user.create")
# @wrapper.wrap("user")
# def create_user() -> User:
#     """
#     创建一个用户的接口调用顺序如下:
#         1. 首先调用创建用户接口 - User(**info...)
#         2. 调用为用户设置密码接口 - auth.Create.withuserid
#         3. 为用户设置文档ID索引 - user.Update.inituser
#     这里密码应该通过 post 参数传入
#     """
#     status: bool = request.form.get("status", default=True, type=bool)
#     password: str = request.form.get("password", default='', type=str)


# @rbac.route("/users/<string:userid>/indexs", methods=["POST"])
# @rbac.route("/users/<string:userid>/status", methods=["POST"])
# @rbac.route("/users/<string:userid>/indexs", methods=["DELETE"])
# @rbac.route("/users/<string:userid>", methods=["DELETE"])
