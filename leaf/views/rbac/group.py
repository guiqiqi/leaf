"""用户组管理视图函数"""

from typing import List, Set

from bson import ObjectId
from flask import request

from . import rbac

from ...api import wrapper
from ...api import validator
from ...core.tools import web
from ...rbac.model import Group
from ...rbac.functions import group as funcs
from ...rbac.functions import user as userfuncs


@rbac.route("/groups/<string:groupid>", methods=["GET"])
@wrapper.require("leaf.views.rbac.group.query")
@wrapper.wrap("group")
def query_group_byid(groupid: str) -> Group:
    """根据给定的 id 查找用户组"""
    groupid = validator.objectid(groupid)
    return funcs.Retrieve.byid(groupid)


@rbac.route("/groups", methods=["GET"])
@wrapper.require("leaf.views.rbac.group.list")
@wrapper.wrap("groups")
def list_all_groups() -> List[Group]:
    """列出所有的用户组信息"""
    # pylint: disable=no-member
    return Group.objects


@rbac.route("/groups/name/<string:name>", methods=["GET"])
@wrapper.require("leaf.views.rbac.group.query")
@wrapper.wrap("groups")
def query_group_byname(name: str) -> List[Group]:
    """根据名称查找指定的用户组"""
    # pylint: disable=no-member
    return Group.objects(name=name)


@rbac.route("/groups/<string:groupid>", methods=["DELETE"])
@wrapper.require("leaf.views.rbac.group.delete")
@wrapper.wrap("status")
def delete_group(groupid: str) -> bool:
    """删除某一个特定的用户组"""
    groupid = validator.objectid(groupid)
    group: Group = funcs.Retrieve.byid(groupid)
    return group.delete()


@rbac.route("/groups", methods=["POST"])
@wrapper.require("leaf.views.rbac.group.add")
@wrapper.wrap("group")
def add_group() -> Group:
    """"增加一个用户组"""
    name: str = request.form.get("name", type=str, default='')
    description: str = request.form.get("description", type=str, default='')
    permission: int = request.form.get("permission", type=int, default=0)
    group: Group = Group(name, description, permission)
    return group.save()


@rbac.route("/groups/<string:groupid>", methods=["PUT"])
@wrapper.require("leaf.views.rbac.group.update")
@wrapper.wrap("group")
def update_group(groupid: str) -> Group:
    """更新某一个用户组的信息"""
    groupid = validator.objectid(groupid)
    group: Group = funcs.Retrieve.byid(groupid)
    name: str = request.form.get("name", type=str, default='')
    description: str = request.form.get("description", type=str, default='')
    permission: int = request.form.get("permission", type=int, default=0)
    group.name = name
    group.description = description
    group.permission = permission
    return group.save()


@rbac.route("/groups/<string:groupid>/users", methods=["PUT"])
@wrapper.require("leaf.views.rbac.group.edituser")
@wrapper.wrap("group")
def add_users_to_group(groupid: str) -> Group:
    """
    编辑用户组中的用户:
        计算所有增加的用户 - 对所有的增加用户进行加组操作
        计算所有被移出组的用户 - 对所有的移出用户进行移出操作
    """
    groupid = validator.objectid(groupid)
    group: Group = funcs.Retrieve.byid(groupid)
    raw: List[str] = [str(user) for user in group.users]
    new: List[str] = web.JSONparser(request.form.get("users"))

    # 集合计算增加与移除的部分
    removed: Set[ObjectId] = set(raw) - set(new)
    added: Set[ObjectId] = set(new) - set(raw)

    # 给用户添加组信息
    for userid in added:
        userfuncs.Create.group(userid, groupid)
    for userid in removed:
        userfuncs.Delete.group(userid, groupid)

    # 返回更新之后的用户组信息
    return funcs.Retrieve.byid(groupid)
