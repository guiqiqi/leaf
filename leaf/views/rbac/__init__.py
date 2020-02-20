"""关于 RBAC 相关的视图函数"""

# pylint: disable=wrong-import-position

rbac = __import__("flask").Blueprint("rbac", __name__)

from . import user
from . import jwt
from . import group
from . import auth
from . import accesspoint
