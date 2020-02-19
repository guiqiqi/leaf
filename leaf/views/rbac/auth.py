"""控制用户的认证相关数据"""

from typing import List, Tuple
from flask import g
from flask import request

from . import rbac
from . import error

from ...api import wrapper
from ...api import settings
from ...rbac.model import UserIndex
from ...rbac.functions import error as rbacerror
from ...rbac.functions import auth as authfuncs
from ...rbac.functions import user as userfuncs


@rbac.route("/auths/<string:userid>/<string:typeid>", methods=["POST"])
@wrapper.require("leaf.views.rbac.auth.create")
@wrapper.wrap("status")
def create_auth_with_user_index(userid: str, typeid: str) -> bool:
    """根据用户的某一个 index 创建 Auth 文档"""
    user = userfuncs.Retrieve.byid(userid)
    index: UserIndex = user.indexs.get(typeid=typeid)
    password: str = request.form.get("password", type=str, default='')
    description: str = request.form.get("description", type=str,
                                        default=index.description)
    authfuncs.Create.withother(index.value, userid,
                               password, description=description)
    return True


@rbac.route("/auths/<string:index>/status", methods=["PUT"])
@wrapper.require("leaf.views.rbac.atuh.update")
@wrapper.wrap("status")
def update_status_for_authdoc(index: str) -> bool:
    """更新用户的认证文档状态"""
    status: bool = request.form.get("status", type=bool, default=True)
    authdoc = authfuncs.Retrieve.byindex(index)
    authdoc.status = status
    authdoc.save()
    return True


@rbac.route("/auths/<string:index>", methods=["DELETE"])
@wrapper.require("leaf.views.rbac.auth.delete", byuser=True)
@wrapper.wrap("status")
def delete_authdoc(index: str) -> bool:
    """删除用户的某一种认证方式"""
    userid: str = request.form.get("userid", type=str)

    # 检查是否由本人发起
    if userid != g.userid:
        return settings.Authorization.UnAuthorized(
            error.AuthenticationError(g.userid))

    authfuncs.Delete.byindex(userid, index)
    return True


@rbac.route("/auths/<string:userid>", methods=["GET"])
@wrapper.require("leaf.views.rbac.auth.get")
@wrapper.wrap("auths")
def query_auth_map_with_userid(userid: str) -> List[Tuple[UserIndex, bool]]:
    """
    查询用户的索引与认证文档的对应状态
    返回类似下面的返回值:
        [(UserIndex1, True), (UserIndex2, False), ...]
    """
    user = userfuncs.Retrieve.byid(userid)
    indexs: List[UserIndex] = user.indexs
    mapping: List[Tuple[UserIndex, bool]] = list()

    for index in indexs:
        try:
            authfuncs.Retrieve.byindex(index.value)
        except rbacerror.AuthenticationNotFound as _error:
            continue
        else:
            mapping.append((index, True))

    return mapping


@rbac.route("/auths/<string:userid>/password", methods=["PUT"])
@wrapper.require("leaf.views.rbac.auth.update", byuser=True)
@wrapper.wrap("status")
def update_password(userid: str) -> bool:
    """更新用户密码"""

    # 检查是否由本人发起
    if userid != g.userid:
        return settings.Authorization.UnAuthorized(
            error.AuthenticationError(g.userid))

    current: str = request.form.get("current", type=str)
    new: str = request.form.get("new", type=str)
    authfuncs.Update.password(userid, current, new)
    return True
