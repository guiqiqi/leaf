"""微信公众平台用户相关API支持"""

from typing import Iterable, Optional

from ...core.tools import web
from .. import settings
from ..const import Request


class User:
    """
    微信公众平台用户相关功能支持:
        remark - 给用户设置备注
        info - 获取单个用户信息
        patch - 批量获取用户信息
    """
    @staticmethod
    def remark(accesstoken: str, openid: str, name: str) -> dict:
        """
        给用户设置新的备注名:
            openid: 用户的 openid
            name: 用户的新昵称
        """
        # 创建发送地址和发送数据
        address = "https://api.weixin.qq.com/cgi-bin/user/info/updateremark"
        data = web.JSONcreater({
            Request.User.OpenID: openid,
            Request.User.Remark: name
        })

        # 发送请求
        response, _ = web.post(
            address, {Request.AccessToken: accesstoken}, data)
        response = web.JSONparser(response)
        return response

    @staticmethod
    def info(accesstoken: str, openid: str,
             language: Optional[str] = settings.User.Language) -> dict:
        """
        获取单个用户信息:
            openid: 要获取信息的用户openid
        """
        # 创建发送数据
        address = "https://api.weixin.qq.com/cgi-bin/user/info"
        data = {
            Request.AccessToken: accesstoken,
            Request.User.OpenID: openid,
            Request.User.Language: language
        }

        # 发送数据
        response, _ = web.get(address, data)
        response = web.JSONparser(response)
        return response

    @staticmethod
    def patch(accesstoken: str, openids: Iterable,
              language: Optional[str] = settings.User.Language) -> dict:
        """
        批量获取用户信息:
            openids: 批量获取信息的用户 openid 列表
        """
        # 创建发送数据
        address = "https://api.weixin.qq.com/cgi-bin/user/info/batchget"

        # 按照微信的官方格式转换信息
        userlist = list()
        data = {Request.User.UserList: userlist}
        for openid in openids:
            userlist.append({
                Request.User.OpenID: openid,
                Request.User.Language: language
            })

        # 发送数据
        request = web.JSONcreater(data)
        response, _ = web.post(
            address, {Request.AccessToken: accesstoken}, request)
        response = web.JSONparser(response)
        return response

    @staticmethod
    def userlist(accesstoken: str, starting: Optional[str] = None) -> dict:
        """
        获取关注公众号的用户 OpenID 列表:
            starting: 获取的第一个用户 OpenID - 不填则为从第一个开始
        """
        # 创建发送数据
        address = "https://api.weixin.qq.com/cgi-bin/user/get"
        if starting:
            params = {
                Request.AccessToken: accesstoken,
                Request.User.StartingPosition: starting
            }
        else:
            params = {
                Request.AccessToken: accesstoken
            }

        # 发送数据
        response, _ = web.get(address, params)
        response = web.JSONparser(response)
        return response
