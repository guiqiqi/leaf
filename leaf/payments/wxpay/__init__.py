"""
微信支付模块:
    payment - 主要支付模块
    signature - 微信支付签名工具
    settings - 微信支付相关设置
    methods - 微信支付方式
    const - 微信支付常量描述
"""

from . import payment
from . import methods
from . import signature

from . import const
from . import settings

signature = signature.SignatureTool
methods = methods.WXPaymentType
payment = payment.WXPayment
