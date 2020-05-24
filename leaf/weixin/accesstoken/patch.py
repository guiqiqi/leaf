"""AccessToken 获取与缓存器"""

import json
import logging
from typing import NoReturn

from . import error
from . import const
from . import settings

from ...core import modules
from ...core import schedule
from ...core.tools import web
from ...core.tools import time
from ...core.error import Messenger


logger = logging.getLogger("leaf.weixin.accesstoken")


class Patcher:
    """
    Leaf 微信公众平台 AccessToken 获取插件:
        get - 获取当前已经缓存的 Token
        stop - 停止任务的继续运行
        update - 手动更新一次 ACToken 缓存
    """

    def __init__(self, appid: str, secret: str):
        """
        获取器构造函数:
            appid - 微信公众平台提供的公众号 AppId
            secret - 微信公众平台提供的 AppSecret
        通过创建 leaf 的计划任务来进行更新
        """
        self.__status = False

        # 保存 APPID SECRET
        self.__appid = appid
        self.__secret = secret

        # 已经保存的缓存与过期时间
        self.__cache = str()
        self.__expire = 0

        # 设置 schedule 模块进行自动更新
        self.__work: schedule.Worker = schedule.Worker(
            self._do, settings.Gap)

    def set(self, cache: str, expire: int) -> NoReturn:
        """手动设置当前的 AccessToken 信息"""
        self.__cache = cache
        self.__expire = expire + time.now()

    def start(self):
        """开始任务执行"""
        manager: schedule.Manager = modules.schedules
        manager.start(self.__work)
        self.__status = True

    def _do(self, retires: int = settings.MaxRetries) -> NoReturn:
        """
        经过包装的 update 函数
        有一个默认参数 retires = settings.MaxRetires
        当 update 执行遇到错误时则将 retries 减一递归
        当 retires = 0 时停止任务运行
        """
        if retires == 0:
            self.stop()
            return

        try:
            self.update()
        except error.Error as _error:
            logger.error(_error)
            self._do(retires - 1)

    def update(self) -> str:
        """
        AccessToken 插件获取函数
        通过 web.get 更新 ACToken 的值并进行更新
        当遇到错误之后进行指定次数的重试
        """

        request = {
            const.GRANT_TYPE: const.TYPE,
            const.APPID: self.__appid,
            const.SECRET: self.__secret
        }  # 请求的 GET 参数

        data, response = web.get(settings.Address, request)

        # 遇到网络错误
        if response.code != 200:
            failed = modules.events.event("leaf.weixin.accesstoken.failed")
            failed.boardcast()
            raise error.AConnectionError(response.code)

        # 尝试解析数据
        try:
            info: dict = web.JSONparser(data)
            token: str = info[const.TOKEN]
            expires: int = int(info[const.EXPIRES])
        except json.decoder.JSONDecodeError as _error:
            raise error.InvalidResponse(_error)
        except KeyError as _error:
            # 这时微信平台返回了异常提示
            code = int(info.get(const.CODE, 0))
            message = info.get(const.MESSAGE, '')
            raiser: Messenger = modules.error.messenger
            raise raiser.error(code, message=message)

        # 更新缓存 - 由广播通知的 update 事件处理
        # self.__cache = token
        # self.__expire = expires + time.now()

        # 发送事件通知
        updated = modules.events.event("leaf.weixin.accesstoken.updated")
        updated.boardcast(token, expires)

        return self.__cache

    def stop(self) -> NoReturn:
        """
        停止获取任务
        发送任务停止通知
        """
        if self.__status is False:
            return

        self.__work.stop()
        self.__status = False

        stopped = modules.events.event("leaf.weixin.accesstoken.stopped")
        stopped.boardcast()

    def restart(self) -> NoReturn:
        """
        先设置任务停止
        之后重启任务
        """
        # 这里不能调用 self.stop
        # 函数会触发事件通知使得插件状态失效
        self.__work.stop()
        self.__work.start()

    @property
    def status(self) -> bool:
        """返回当前更新器是否在工作"""
        return self.__status

    def get(self) -> str:
        """
        返回缓存的 APPID
        """
        if self.__expire == 0 and not self.__status:
            raise error.ReachedMaxRetries("经过多次失败之后, 更新器已经停止工作")

        if self.__expire == 0:
            raise error.AccessTokenStatusError("正在获取token, 请稍后再试")

        if time.now() > self.__expire:
            raise error.AccessTokenStatusError("当前缓存已经超时且无法更新")

        return self.__cache
