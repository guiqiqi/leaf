"""有关权限验证使用到的函数集合"""

from functools import lru_cache
from typing import List, Optional

from bson import ObjectId

from . import error
from ...core.tools import encrypt
from ..model import Authentication
from ..settings import Authentication as settings


class Generator:
    """
    口令验证器 - 使用加密策略计算口令
    加密策略:
        密码 + 盐值作为初始密码
        迭代SHA256算法对初始密码进行哈希指定次数
    """

    @staticmethod
    def calc(password: str, salt: str) -> str:
        """根据盐和密码计算口令"""
        return Generator.shahash(password + salt)

    @staticmethod
    def shahash(previous: str, depth: Optional[int]
                = settings.Security.PasswordHashCycle) -> str:
        """对密码进行迭代hash"""
        if depth != 0:
            return Generator.shahash(previous, depth - 1)
        return previous


class Create:
    """创建静态函数集合"""

    @staticmethod
    def withuserid(userid: ObjectId, password: str) -> Authentication:
        """
        通过用户ID创建验证文档
        当一个用户被创建之后, 需要同步的创建该文档
        之后的密码验证需要以该文档作为基础
        该文档的登陆验证登陆选项默认是禁用
        """
        salt = encrypt.random(settings.Security.SaltLength / 8)
        index = encrypt.base64encode(str(userid))
        auth = Authentication(
            index=index, user=userid,
            salt=salt, token=Generator.calc(password, salt),
            status=False, description=settings.Description.Id)
        return auth.save()

    @staticmethod
    def withother(index: str, userid: ObjectId, password: str,
                  status: Optional[bool] = True,
                  description: Optional[str] = str()):
        """
        使用其他的方式创建验证文档:
            首先获取 Id 方式创建的密码文档并验证当前密码是否正确
            如果不正确则 raise 错误
            正确则按照信息保存新的身份文档
        """
        # pylint: disable=no-member
        authbyid: Authentication = Authentication.objects(index=str(userid))
        if not authbyid:
            raise error.AuthenticationByIdFailed(str(userid))
        if Generator.calc(password, authbyid.salt) != authbyid.token:
            raise error.AuthenticationFailed(password)

        # 创建文档
        salt = encrypt.random(settings.Security.SaltLength / 8)
        index = encrypt.base64encode(index)
        auth = Authentication(
            index=index, user=userid,
            salt=salt, token=Generator.calc(password, salt),
            status=status, description=description)
        return auth.save()


class Retrieve:
    """查找静态函数集合"""

    @staticmethod
    @lru_cache(typed=False)
    def byindex(index: str) -> Optional[Authentication]:
        """根据认证索引查找认证信息 - 缓存"""
        index = encrypt.base64encode(index.encode()).decode()
        # pylint: disable=no-member
        found: List[Authentication] = Authentication.objects(index=index)
        if not found:
            return None
        return found.pop()

    @staticmethod
    def byuser(userid: ObjectId) -> List[Authentication]:
        """根据用户 userid 查找对应的认证方式集合"""
        # pylint: disable=no-member
        return Authentication.objects(user=userid)
