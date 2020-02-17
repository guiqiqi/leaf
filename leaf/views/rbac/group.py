"""用户组管理视图函数"""

from typing import List, Set
from flask import request
from bson import ObjectId
from . import rbac

from ...api import wrapper
from ...rbac.model import User
from ...rbac.model import Group
from ...rbac.functions import group as funcs
from ...rbac.functions import user as user_funcs


@rbac.route("/groups/<string:groupid>", methods=["GET"])
@wrapper.require("leaf.views.rbac.group.query")
@wrapper.wrap("group")
def query_group_byid(groupid: str) -> Group:
    """根据给定的 id 查找用户组"""
    return funcs.Retrieve.byid(groupid)


@rbac.route("/groups", methods=["GET"])
@wrapper.require("leaf.views.rbac.group.list")
@wrapper.wrap("groups")
def list_all_groups() -> List[Group]:
    """列出所有的用户组信息"""
    # pylint: disable=no-member
    return Group.objects


@rbac.route("/groups/<string:name>", methods=["GET"])
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
    """编辑用户组中的用户"""
    group: Group = funcs.Retrieve.byid(groupid)
    users: List[User] = request.form.getlist("users", type=ObjectId)

    # 计算多增加的那一部分 - 用集合的差计算
    # 原有用户列表 {1, 2, 3} - 现有新用户列表 {2, 3, 4}
    # 需要检查的仅为 {4} = {2, 3, 4} - {1, 2, 3}
    diff: Set[ObjectId] = set(users) - set(group.users)

    # 检查是否所有的用户都存在 - 给用户添加组信息
    for userid in diff:
        user: User = user_funcs.Retrieve.byid(userid)
        user.groups.append(group)
        user.save()

    group.users = users
    return group.save()
