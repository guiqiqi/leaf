"""微信支付方式"""

from typing import NoReturn
from . import const


class WXPaymentType:
    """支付类型补充函数"""
    @staticmethod
    def jsapi(orderinfo: dict) -> NoReturn:
        """
        静态函数 - 对支付信息添加支付类型信息 - jaspi
        *orderinfo:dict - 支付信息字典
        """
        orderinfo[const.WXPayOrder.Info.Type] = \
            const.WXPayOrder.Type.JSAPI

    @staticmethod
    def native(orderinfo: dict) -> NoReturn:
        """
        静态函数 - 对支付信息添加支付类型信息 - native
        *orderinfo:dict - 支付信息字典
        """
        orderinfo[const.WXPayOrder.Info.Type] = \
            const.WXPayOrder.Type.ScanQR

    @staticmethod
    def inapp(orderinfo: dict) -> NoReturn:
        """
        静态函数 - 对支付信息添加支付类型信息 - inapp
        *orderinfo:dict - 支付信息字典
        """
        orderinfo[const.WXPayOrder.Info.Type] = \
            const.WXPayOrder.Type.InApp
