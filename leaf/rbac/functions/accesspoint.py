"""访问点所需要的函数集合"""

from typing import Optional, List
from ..model import AccessPoint


def byname(name: str) -> Optional[AccessPoint]:
    """根据名称查找访问点"""
    # pylint: disable=no-member
    found: List[AccessPoint] = AccessPoint.objects(pointname=name)
    if not found:
        return None
    return found.pop()
