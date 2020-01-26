"""
微信公众平台消息回复制作器
"""

from typing import Optional, List
from .. import const


class MakeReply:
    """
    制作消息回复包
    制作出的消息返回值格式为:
        msgtype: str - 消息类型
        msg: dict - 返回的消息
    函数调用示例:
        MakeReply.text("HELLO WORLD!") ->
        ("text", {"Content": "HELLO WORLD!"})
    """
    @staticmethod
    def text(content: str) -> dict:
        """
        回复文本消息:
            content: 回复内容
        """
        return {
            const.Message.Type: const.Reply.Types.Text,
            const.Reply.Text.Key: content
        }

    @staticmethod
    def picture(mediaid: str) -> dict:
        """
        回复图片消息:
            mediaid: 图片mediaid
        """
        return {
            const.Message.Type: const.Reply.Types.Image,
            const.Reply.Image.Key: {
                const.Reply.Image.MediaId: mediaid
            }
        }

    @staticmethod
    def voice(mediaid: str) -> dict:
        """
        回复语音消息:
            mediaid: 语言 mediaid
        """
        return {
            const.Message.Type: const.Reply.Types.Voice,
            const.Reply.Types.Voice: {
                const.Reply.Voice.MediaId: mediaid
            }
        }

    @staticmethod
    def video(mediaid: str, title: Optional[str] = None,
              description: Optional[str] = None) -> dict:
        """
        回复视频消息:
            mediaid: 视频 mediaid
            title: 标题 - 可选
            description: 描述 - 可选
        """
        content = {const.Reply.Video.MediaId: mediaid}

        # 如果有附加的键则添加消息
        if not title is None:
            content[const.Reply.Video.Title] = title
        if not description is None:
            content[const.Reply.Video.Description] = description

        return {
            const.Message.Type: const.Reply.Types.Video,
            const.Reply.Types.Video: content
        }

    @staticmethod
    def music(thumb: str, title: Optional[str] = None,
              description: Optional[str] = None,
              url: Optional[str] = None,
              HQ: Optional[str] = None) -> dict:
        """
        回复音乐消息:
            thumb: 缩略图mediaid
            title: 标题 - 可选
            description: 描述 - 可选
            url: 地址 - 可选
            HQ: 高清地址 - 可选
        """
        content = {const.Reply.Music.Thumb: thumb}

        # 添加可选信息
        if not title is None:
            content[const.Reply.Music.Title] = title
        if not description is None:
            content[const.Reply.Music.Description] = description
        if not url is None:
            content[const.Reply.Music.URL] = url
        if not HQ is None:
            content[const.Reply.Music.HQURL] = HQ

        return {
            const.Message.Type: const.Reply.Types.Music,
            const.Reply.Types.Music: content
        }

    @staticmethod
    def article(title: str, description: str,
                image: str, redirect: str) -> dict:
        """
        生成一条文章回复:
            title: 文章标题
            description: 文章描述
            image: 图片地址
            redirect: 跳转地址
        *请勿单独调用该函数作为回复
        *请将结果传入 articles 函数包装
        """
        return {
            const.Reply.Article.Item.Title: title,
            const.Reply.Article.Item.Picture: image,
            const.Reply.Article.Item.URL: redirect,
            const.Reply.Article.Item.Descritpion: description
        }

    @staticmethod
    def articles(articles: List[dict]) -> dict:
        """
        回复图文消息:
            articles: 使用 article 函数生成的字典列表
        """
        data = [{const.Reply.Article.Item.Key: item} for item in articles]
        return {
            const.Reply.Article.Count: len(articles),
            const.Reply.Types.Article: data
        }
