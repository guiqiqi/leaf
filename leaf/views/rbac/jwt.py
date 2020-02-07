"""JWT 视图函数"""

import logging
from typing import List

from flask import request
from bson import ObjectId

from . import rbac
from . import error

from ...api import wrapper
from ...core import events
from ...core import modules

from ...rbac import jwt
from ...rbac.model import Group
from ...rbac.functions import user
from ...rbac.functions import auth

# 获取事件与日志管理器
manager: events.Manager = modules.events
logger = logging.getLogger("leaf.views.rbac.jwt")

issued = events.Event("leaf.rbac.jwt.token.issued", ((ObjectId,), {}),
                      description="签发了一个 JWT Token")
failed = events.Event("leaf.rbac.jwt.token.authfailed", ((str, str), {}),
                      description="在签发时遇到了验证错误")
manager.add(issued)
manager.add(failed)


@rbac.route("/jwt/issue/<string:usertoken>", methods=["POST"])
@wrapper.wrap("token")
def issue_jwt_token(usertoken: str) -> str:
    """为指定的用户颁发 JWT Token"""
    password: str = request.form.get("password", default=str(), type=str)
    validation = auth.Generator.valid(usertoken, password)
    if not validation:
        failed.notify(usertoken, password)
        raise error.AuthenticationError(usertoken)

    # 获取认证信息
    authdoc = auth.Retrieve.byindex(usertoken)
    if not authdoc.status:
        failed.notify(usertoken, password)
        raise error.AuthenticationDisabled(usertoken)
    userid: ObjectId = authdoc.user.id
    salt: str = authdoc.salt

    # 获取用户组权限
    userdoc = user.Retrieve.byid(userid)
    groups: List[Group] = userdoc.groups
    permissions = tuple((group.permission for group in groups))

    # 颁发 Token
    token = jwt.Token(salt)
    token.header()
    token.payload(issuer="leaf.views.jwt", audience=str(userid),
                  other={jwt.settings.Payload.Permission: permissions})
    issued.notify(userid)
    return token.issue()
