"""用户组操作的相关函数集合"""

from typing import List

from bson import ObjectId

from . import error
from ..model.group import Group


class Create:
    """创建用户组的静态函数集合"""


class Retrieve:
    """查询用户组的静态函数集合"""

    @staticmethod
    def byid(groupid: ObjectId) -> Group:
        """通过用户组 ID 查找用户组记录"""
        # pylint: disable=no-member
        found: List[Group] = Group.objets(id=groupid)
        if not found:
            raise error.GroupNotFound(str(groupid))
        return found[0]


class Update:
    """更新/编辑用户组的静态函数集合"""


class Delete:
    """删除用户组的静态函数结合"""
