"""有关权限验证使用到的函数集合"""

from functools import lru_cache
from typing import List, Optional, NoReturn

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
    def valid(index: str, password: str) -> bool:
        """对用户的某一登陆方式进行验证"""
        # pylint: disable=no-member
        auth: Authentication = Authentication.objects(index=index)
        if not auth or Generator.calc(
                password, auth[0].salt) != auth[0].token:
            return False
        return True

    @staticmethod
    def validbyid(userid: ObjectId, password: str) -> NoReturn:
        """通过用户ID文档验证密码是否正确"""
        # pylint: disable=no-member
        authbyid: List[Authentication] = Authentication.objects(
            index=str(userid))
        if not authbyid:
            raise error.AuthenticationByIdFailed(str(userid))
        if Generator.calc(password, authbyid[0].salt) != authbyid[0].token:
            raise error.AuthenticationFailed(password)

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
        # authbyid: Authentication = Authentication.objects(index=str(userid))
        # if not authbyid:
        #     raise error.AuthenticationByIdFailed(str(userid))
        # if Generator.calc(password, authbyid.salt) != authbyid.token:
        #     raise error.AuthenticationFailed(password)
        Generator.validbyid(userid, password)

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
    @lru_cache(maxsize=settings.Security.SaltCahce)
    def saltbyindex(index: str) -> str:
        """根据认证索引查询 - LRU缓存"""
        auth = Retrieve.byindex(index)
        return auth.salt

    @staticmethod
    def byindex(index: str) -> Authentication:
        """根据认证索引查找认证信息"""
        index = encrypt.base64encode(index.encode()).decode()
        # pylint: disable=no-member
        found: List[Authentication] = Authentication.objects(index=index)
        if not found:
            raise error.AuthenticationNotFound(index)
        return found.pop()

    @staticmethod
    def byuser(userid: ObjectId) -> List[Authentication]:
        """根据用户 userid 查找对应的认证方式集合"""
        # pylint: disable=no-member
        return Authentication.objects(user=userid)


class Update:
    """更新静态函数集合"""

    @staticmethod
    def password(userid: ObjectId, old: str, new: str) -> NoReturn:
        """
        更新用户密码:
            根据userid寻找Id验证文档
            验证旧密码是否正确
            不正确则返回错误
            对所有的身份验证文档密码都进行更新
        """
        Generator.validbyid(userid, old)

        # 查找该用户所有的文档都进行更新
        # pylint: disable=no-member
        auths: List[Authentication] = Authentication.objects(user=userid)
        for auth in auths:
            auth.token = Generator.calc(new, auth.salt)
            auth.save()
