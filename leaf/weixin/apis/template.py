"""微信公众平台模板消息API实现"""

from typing import Optional

from ...core.tools import web
from ..const import Request


class TemplateMessage:
    """
    微信公众平台模板消息API实现:
        setindustry - 设置模板所属行业
    """

    @staticmethod
    def setindustry(accesstoken: str, firstid: int, secondid: int) -> dict:
        """
        设置模板消息库所属行业:
            firstid: 第一个行业 id
            secondid: 第二个行业 id
        """
        # 创建发送消息
        address = "https://api.weixin.qq.com/cgi-bin/template/api_set_industry"
        param = {Request.AccessToken: accesstoken}
        data = {
            Request.Template.IndustryFirst: firstid,
            Request.Template.IndustrySecond: secondid
        }
        request = web.JSONcreater(data)

        # 发送消息
        response, _ = web.post(address, param, request)
        response = web.JSONparser(response)
        return response

    @staticmethod
    def getindustry(accesstoken: str) -> dict:
        """
        获取当前设置的行业信息
        """
        # 创建发送消息
        address = "https://api.weixin.qq.com/cgi-bin/template/get_industry"
        param = {Request.AccessToken: accesstoken}

        # 发送消息
        response, _ = web.get(address, param)
        response = web.JSONparser(response)
        return response

    @staticmethod
    def add(accesstoken: str, templateid: str) -> dict:
        """
        向模板库中下载一个模板:
            templateid: 要增加的模板id
        """
        # 创建发送消息
        address = "https://api.weixin.qq.com/cgi-bin/template/api_add_template"
        param = {Request.AccessToken: accesstoken}
        request = {Request.Template.ID: templateid}
        request = web.JSONcreater(request)

        # 发送请求
        response, _ = web.post(address, param, request)
        response = web.JSONparser(response)
        return response

    @staticmethod
    def get(accesstoken: str) -> dict:
        """
        获取本地模板库中所有的模板
        """
        # 创建发送的消息
        address = "https://api.weixin.qq.com/cgi-bin/template/get_all_private_template"
        param = {Request.AccessToken: accesstoken}

        # 发送请求
        response, _ = web.get(address, param)
        response = web.JSONparser(response)
        return response

    @staticmethod
    def delete(accesstoken: str, templateid: str) -> dict:
        """
        删除库中已经下载好的某个模板:
            templateid: 要删除的模板id
        """
        # 创建发送消息
        address = "https://api.weixin.qq.com/cgi-bin/template/del_private_template"
        param = {Request.AccessToken: accesstoken}
        request = {Request.Template.ID: templateid}

        # 发送请求
        response, _ = web.post(address, param, request)
        response = web.JSONparser(response)
        return response

    @staticmethod
    def send(accesstoken: str, touser: str, templateid: str,
             data: dict, url: Optional[str] = None,
             appid: Optional[str] = None,
             pagepath: Optional[str] = None) -> dict:
        """
        请求发送一个模板消息:
            touser: 要发送用户的 openid
            template_id: 要发送的模板 id
            data: 要发送的模板数据
            url: 跳转的网页链接
            appid: 要跳转的小程序 appid
            miniprogram: 要跳转的小程序数据
            pagepath: 要跳转的小程序路径
        *注意:
            后面两个参数用来指定小程序跳转的相关参数,
            当不指定时不进行跳转, 要提供时需要一起提供
        *data数据格式:
            {
                "格式化参数": ("数据", "颜色代码"),
                "first": ("您已经订阅成功", "#CCCAAA"),
                ...
            }
        """
        # 准备发送数据
        address = "https://api.weixin.qq.com/cgi-bin/message/template/send"
        param = {Request.AccessToken: accesstoken}
        sendata = dict()

        # 遍历生成数据
        for key, parameter in data.items():
            item, color = parameter
            sendata[key] = {
                Request.Template.Data.Value: item,
                Request.Template.Data.Color: color
            }

        request = {
            Request.Template.Data.Key: sendata,
            Request.Template.ToUser: touser,
            Request.Template.ID: templateid,
        }

        # 添加链接跳转
        if not url is None:
            request[Request.Template.JumpTo] = url

        # 添加小程序跳转信息
        if appid and pagepath:
            miniprogram = {
                Request.MiniProgram.AppID: appid,
                Request.MiniProgram.PagePath: pagepath
            }
            request[Request.Template.MiniProgram] = miniprogram

        request = web.JSONcreater(request)

        # 发送数据
        response, _ = web.post(address, param, request)
        response = web.JSONparser(response)
        return response
