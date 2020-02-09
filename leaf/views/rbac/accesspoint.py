"""AccessPoint 模型视图函数"""

from typing import List, Set

from flask import request
from bson import ObjectId
from mongoengine import NotUniqueError

from . import rbac
from . import error

from ...api import wrapper
from ...rbac.model import AccessPoint
from ...rbac.functions import user
from ...rbac.functions import accesspoint as funcs


@rbac.route("/accesspoints/<string:pointname>", methods=["GET"])
@wrapper.require("leaf.views.rbac.accesspoint.query")
@wrapper.wrap("accesspoint")
def query_accesspoint_byname(pointname: str) -> AccessPoint:
    """根据指定的名称查找相关的访问点信息"""
    point: AccessPoint = funcs.Retrieve.byname(pointname)
    return point


@rbac.route("/accesspoints", methods=["GET"])
@wrapper.require("leaf.views.rbac.accesspoint.getall")
@wrapper.wrap("accesspoints")
def getall_accesspoints() -> List[AccessPoint]:
    """返回所有的访问点信息"""
    # pylint: disable=no-member
    return list(AccessPoint.objects)


@rbac.route("/accesspoints/<string:pointname>", methods=["DELETE"])
@wrapper.require("leaf.views.rbac.accesspoint.delete")
@wrapper.wrap("status")
def delete_accesspoint(pointname: str) -> bool:
    """删除某一个访问点信息"""
    point: AccessPoint = funcs.Retrieve.byname(pointname)
    point.delete()
    return True


@rbac.route("/accesspoints", methods=["POST"])
@wrapper.require("leaf.views.rbac.accesspoint.create")
@wrapper.wrap("accesspoint")
def create_accesspoint() -> AccessPoint:
    """创建一个访问点信息"""
    pointname: str = request.form.get("pointname", type=str, default='')
    required: int = request.form.get("required", type=int, default=0)
    strict: bool = request.form.get("strict", type=bool, default=False)
    description: str = request.form.get("description", type=str, default='')

    try:
        point: AccessPoint = AccessPoint(
            pointname, required, strict, description)
        return point.save()
    except NotUniqueError as _error:
        raise error.AccessPointNameConflicting(pointname)


@rbac.route("/accesspoints/<string:pointname>", methods=["PUT"])
@wrapper.require("leaf.views.rbac.accesspoint.update")
@wrapper.wrap("accesspoint")
def update_accesspoint(pointname: str) -> AccessPoint:
    """更新某一个访问点信息"""
    required: int = request.form.get("required", type=int, default=0)
    strict: bool = request.form.get("strict", type=bool, default=False)
    description: str = request.form.get("description", type=str, default='')

    point: AccessPoint = funcs.Retrieve.byname(pointname)
    point.required = required
    point.strict = strict
    point.description = description
    point: AccessPoint = AccessPoint(pointname=pointname, required=required,
                                     strict=strict, description=description)

    return point.save()


@rbac.route("/accesspoints/<string:pointname>/exception", methods=["PUT"])
@wrapper.require("leaf.views.rbac.accesspoint.exception")
@wrapper.wrap("accesspoint")
def add_exception_user_for_accesspoint(pointname: str) -> AccessPoint:
    """为指定的 AccessPoint 管理特权用户"""
    point: AccessPoint = funcs.Retrieve.byname(pointname)
    exceptions: List[str] = request.form.getlist("exceptions", type=ObjectId)
    diff: Set[ObjectId] = set(exceptions) - set(point.exception)

    # 检查每一个用户是否都存在
    for userid in diff:
        user.Retrieve.byid(userid)

    point.exception = exceptions
    return point.save()
