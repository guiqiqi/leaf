"""微信公众平台常量说明"""


class Encrypt:
    """加密相关常量"""
    PadLength = 16  # 微信默认的 Pad 补位长度

    class URL:
        """URL中的参数设置"""

        class Key:
            """URL 中的参数key"""
            Echo = "echostr"  # 第一次请求的回显消息键
            Encrypted = "encrypt_type"  # URL 中用来判断是否加密的参数
            TimeStamp = "timestamp"  # 时间戳
            Nonce = "nonce"  # 随机数键
            Signature = "msg_signature"  # 消息签名验证键

        class Value:
            """URL 中的参数设定"""
            Encrypted = "aes"  # 在请求的 URL 参数中判定是否加密
            NotEncrypted = "raw"  # 请求 URL 中判定未经过加密

    class Message:
        """消息中的加密相关设置"""
        Content = "Encrypt"  # 加密消息的存储键
        Nonce = "Nonce"  # 消息中的随机数键
        Signature = "MsgSignature"  # 消息中的签名键
        TimeStamp = "TimeStamp"  # 消息中的时间戳键


class Reply:
    """回复中的常量定义"""

    class Types:
        """回复类型定义"""
        Text = "text"  # 文本消息
        Image = "image"  # 图片消息
        Voice = "voice"  # 语音消息
        Video = "video"  # 视频消息
        Music = "music"  # 音乐消息
        Article = "news"  # 图文消息

    class Text:
        """文本消息回复"""
        Key = "Content"

    class Image:
        """图片消息回复"""
        Key = "Image"
        MediaId = "MediaId"  # 素材id

    class Voice:
        """语音消息回复"""
        Key = "Voice"
        MediaId = "MediaId"  # 素材id

    class Video:
        """视频消息回复"""
        Key = "Video"
        MediaId = "MediaId"  # 素材id
        Title = "Title"  # 视频标题
        Description = "Description"  # 视频描述

    class Music:
        """音乐消息回复"""
        Key = "Music"
        Title = "Title"  # 音乐标题
        Description = "Description"  # 描述
        URL = "MusicUrl"  # 音乐链接
        HQURL = "HQMusicUrl"  # 高质量音乐链接
        Thumb = "ThumbMediaId"  # 缩略图媒体ID

    class Article:
        """图文消息回复"""
        Key = "Article"
        Count = "ArticleCount"  # 消息数量

        class Item:
            """图文消息"""
            Key = "Item"
            Title = "Title"  # 回复消息标题
            Descritpion = "Description"  # 消息描述
            Picture = "PicUrl"  # 图片地址
            URL = "Url"  # 跳转地址


class Event:
    """事件通知相关常量"""

    Type = "Event"  # 事件类型提取键

    # 需要拉动的事件类型记录
    Events = {
        "subcribe": "leaf.weixin.events.subscribe",
        "unsubscribe": "leaf.weixin.events.unsubscribe",
        "SCAN": "leaf.weixin.events.scan",
        "LOCATION": "leaf.weixin.events.location",
        "CLICK": "leaf.weixin.events.menu.click",
        "VIEW": "leaf.weixin.events.menu.view",
        "TEMPLATESENDJOBFINISH": "leaf.weixin.events.pushed",
    }

    # 需要获取的键记录
    Types = {
        "subcribe": {},
        "unsubcribe": {},
        "SCAN": {
            "EventKey": "key",
            "Ticket": "ticket"
        },
        "LOCATION": {
            "Latitude": "latitude",
            "Longitude": "longitude",
            "Precision": "precision"
        },
        "CLICK": {
            "EventKey": "key"
        },
        "VIEW": {
            "EventKey": "key"
        },
        "TEMPLATESENDJOBFINISH": {
            "MsgID": "id"
        }
    }


class Message:
    """消息体中的相关常量"""

    Root = "xml"

    Event = "AppId"  # 存在该键表示消息类型为事件
    Message = "ToUserName"  # 存在该键表示为消息

    To = "ToUserName"  # 发往
    From = "FromUserName"  # 从...发来
    CreateTime = "CreateTime"  # 消息何时创建
    Type = "MsgType"  # 消息类型键
    Id = "MsgId"  # 消息 ID 键

    # 需要获取的键记录
    Types = {
        # 文本类型的消息
        "text": {
            "Content": "content"  # 文本消息体
        },

        # 图片类型的消息
        "image": {
            "PicUrl": "url",  # 图片的 URL
            "MediaId": "id"  # 图片媒体ID
        },

        # 语音类型的消息
        "voice": {
            "MediaId": "id",  # 语音媒体ID
            "Format": "format",  # 语音格式
            "Recognition": "recognition",  # 识别之后的语音
        },

        # 视频类型的消息
        "video": {
            "MediaId": "id",  # 视频媒体ID
            "ThumbMediaId": "thumb",  # 视频缩略图媒体ID
        },

        # 小视频消息
        "shortvideo": {
            "MediaId": "id",  # 视频媒体ID
            "ThumbMediaId": "thumbid",  # 视频缩略图媒体ID
        },

        # 地理位置消息
        "location": {
            "Location_X": "latitude",  # 纬度
            "Location_Y": "longitude",  # 经度
            "Scale": "scale",  # 地图缩放大小
            "Label": "label"  # 地理位置消息
        },

        # 链接类型消息
        "link": {
            "Title": "title",  # 链接标题
            "Description": "description",  # 链接描述
            "Url": "url"  # 链接地址
        }
    }


class Request:
    """请求相关常量"""
    AccessToken = "access_token"

    class User:
        """用户相关请求"""
        OpenID = "openid"  # 用户 OpenID
        Language = "lang"  # 获取信息的语言版本
        Remark = "remark"  # 用户昵称
        UserList = "user_list"  # 批量获取用户信息
        StartingPosition = "next_openid"  # 开始获取的 OpenID

    class Template:
        """模板消息相关请求"""
        IndustryFirst = "industry_id1"  # 主行业 ID
        IndustrySecond = "industry_id2"  # 副行业 ID
        ID = "template_id"  # 要调取的 TemplateID
        ToUser = "touser"  # 要发送的用户 OpenID
        JumpTo = "url"  # 跳转的页面链接
        MiniProgram = "miniprogram"  # 小程序数据

        class Data:
            """发送数据子项目"""
            Key = "data"  # 要发送的模板数据键
            Value = "value"  # 要发送的数据值
            Color = "color"  # 要发送的数据颜色

    class MiniProgram:
        """小程序相关请求"""
        AppID = "appid"  # 小程序 AppID
        PagePath = "pagepath"  # 小程序路径
