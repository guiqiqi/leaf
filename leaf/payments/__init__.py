"""
支付方式集合:
    wxpay - 符合 leaf.payment 抽象的微信支付模块
    alipay - 符合 leaf.payment 抽象的支付宝支付模块
"""

from . import wxpay
from . import alipay
from . import yandex
