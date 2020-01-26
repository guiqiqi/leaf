"""针对微信支付平台的加密功能"""

import string
import urllib.parse as urlparse
from typing import NoReturn

from ... import core
from . import const
from . import settings


class SignatureTool:
    """微信支付加密模块"""

    def __repr__(self) -> str:
        """返回 repr 信息"""
        return "<Leaf Payments.WXPayment.Signature>"

    def __init__(self, apikey: str):
        """
        加密模块初始化:
            apikey: 微信商户平台 API 密钥
        """
        self.__apikey = apikey

    @staticmethod
    def _calculate(apikey: str, **paras) -> str:
        """
        根据微信公众平台支付加密标准对包进行签名:
        pay.weixin.qq.com/wiki/doc/api/external/*.php?chapter=4_3
            0. 对参数字典中空的值进行处理 - 不参与运算
            1. 对 paras 中传入的参数按照 ASCII 码的大小顺序进行排序
            2. url化参数拼接 + apikey
            3. 进行MD5签名
        """
        # 首先过滤掉空参数
        __calculates = dict()
        for key, value in paras.items():
            if str(value):
                __calculates[str(key)] = str(value)

        # 之后对参数进行排序并添加 apikey
        __sorted = sorted(__calculates.items(), key=lambda item: item[0])
        __sorted.append((const.WXPaySignature.Key.ApiKey, apikey))

        # 对参数进行 URL 化拼接并进行摘要运算
        clearstr = urlparse.urlencode(__sorted, safe=string.punctuation)
        sign = core.tools.encrypt.MD5(clearstr)

        return sign.upper()

    def do(self, unsigned: dict) -> NoReturn:
        """
        为参数字典进行签名
        这里的参数字典不需要携带签名过程中的任何信息:
            1. 随机字符串 - nonce_str
            2. 签名 - sign
            3. 签名类型 - sign_type
        这些信息由签名工具自动生成, 调用者只需要关心业务相关信息
        """
        # 生成一个随机数并添加
        randstr = core.tools.encrypt.random(
            settings.NetworkAndEncrypt.NonceLength)
        unsigned[const.WXPaySignature.Key.Nonce] = randstr

        # 添加固定值 - 这里 Version 会引起不同 API 调用错误 - 取消添加
        # unsigned[const.WXPaySignature.Key.Version] = \
        #     const.WXPaySignature.Value.Version

        unsigned[const.WXPaySignature.Key.Type] = \
            const.WXPaySignature.Value.Type

        # 计算签名
        siganture = self._calculate(self.__apikey, **unsigned)
        unsigned[const.WXPaySignature.Key.Sign] = siganture

    def verify(self, **signed) -> bool:
        """
        对传入的数据包进行数据校验:
            校验成功返回 True 失败返回 False
        实际等同于重新计算一次签名值检查是否相同
        """
        # 获取目标数据包的 Sign 值
        signature_signed = signed.pop(const.WXPaySignature.Key.Sign, None)
        if signature_signed is None:
            return False

        # 重新计算签名
        signature_unsigned = self._calculate(self.__apikey, **signed)

        # 判断是否相同
        return signature_signed == signature_unsigned
