"""访问点所需要的函数集合"""

from typing import List

from . import error
from ..model import AccessPoint


class Create:
    """创建静态函数集合"""


class Retrieve:
    """查找静态函数集合"""

    @staticmethod
    def byname(name: str) -> AccessPoint:
        """根据名称查找访问点"""
        # pylint: disable=no-member
        found: List[AccessPoint] = AccessPoint.objects(pointname=name)
        if not found:
            raise error.AccessPointNotFound(name)
        return found.pop()


class Update:
    """更新静态函数集合"""


class Delete:
    """删除静态函数集合"""
