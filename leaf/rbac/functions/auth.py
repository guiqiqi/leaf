"""有关权限验证使用到的函数集合"""

from functools import lru_cache
from typing import List, Optional
from ..model import Authentication


@lru_cache(typed=False)
def byindex(index: str) -> Optional[Authentication]:
    """根据认证索引查找认证信息 - 缓存"""
    # pylint: disable=no-member
    found: List[Authentication] = Authentication.objects(index=index)
    if not found:
        return None
    return found.pop()
