"""关于 RBAC 相关的视图函数"""

import logging
from flask import Blueprint
rbac = Blueprint("rbac", __name__)

# pylint: disable=wrong-import-position
from . import error

# 将事件提交给事件管理器
from . import jwt
from . import auth
from . import user
from . import group
from . import accesspoint
