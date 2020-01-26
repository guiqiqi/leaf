"""
一个基于微信支付的消息过滤器:
    因为微信支付平台的回传信息是有一定规则的
    所以可以在这一步根据规则检验数据包是否合法
    如果不合法则可以 raise 相关的错误给业务层处理

    同时, 这个过滤器也还可以用作 views 支付视图函数中
    用来处理回调函数的信息过滤
"""

import logging
from xml.etree.ElementTree import ParseError

from flask import Blueprint
from flask import request

from ..core import events
from ..core import modules
from ..core.tools import web

from ..payments.wxpay import const
from ..payments.wxpay import error
from ..payments.wxpay import payment
from ..payments.wxpay import settings
from ..payments.wxpay import signature

# 支付提醒的标准回复
_STANDARD_REPLY = web.XMLcreater({"xml": {
    const.WXPayResponse.Status: const.WXPayResponse.Success,
    const.WXPayResponse.Message: const.WXPayResponse.Nothing
}}, encoding=None)


wxpay = Blueprint("wxpay", __name__)
logger = logging.getLogger("leaf.views.wxpay")


# 注册支付成功与失败提醒事件
# 位置参数列表 - appid, openid, trade_out_no, cash_fee
paysuccess = events.Event(
    "leaf.payments.wxpay.notify.pay.success",
    ((str, str, str, float), {}),
    "支付成功时的结果通知"
)

payfail = events.Event(
    "leaf.payments.wxpay.notify.pay.fail",
    ((str, str, str, float), {}),
    "支付失败时的结果通知"
)

manager: events.Manager = modules.events
manager.add(paysuccess)
manager.add(payfail)


@wxpay.route("/refund_notify", methods=["POST"])
def refund_notify_handler() -> str:
    """处理退款通知"""
    response = request.data.decode(encoding="utf-8", errors="ignore")

    # 暂未获取到官方文档, 在 logger 中打日志
    logger.info("WXPay-refund-notify received: " + response)

    return _STANDARD_REPLY


@wxpay.route("/notify", methods=["POST"])
def payment_notify_handler() -> str:
    """微信支付付款结果通知处理函数"""
    response = request.data.decode(encoding="utf-8", errors="ignore")

    # 防止异常发生
    try:
        response = web.XMLparser(response)
    except ParseError as _error:
        logger.info("WXPay-notify parsing failed: " + response)
        return _STANDARD_REPLY

    response = response.get(const.WXPayAddress.XMLTag, {})

    sigtool: signature = modules.payments.wxpay.signature

    # 校验签名是否正确
    if not sigtool.verify(**response):
        try:
            raise error.WXPaySignatureError(str(response))
        except error.WXPayError as _error:
            logger.error(_error)
            return _STANDARD_REPLY

    # 获取需要的信息
    appid = response.get(const.WXPayBasic.AppID)
    openid = response.get(const.WXPayBasic.OpenID)
    orderid = response.get(const.WXPayOrder.ID.In)
    fee = response.get(const.WXPaymentNotify.Fee)

    kvparas = dict()
    for key, value in settings.PaymentNotify.Keys.items():
        kvparas[value] = response.get(key)

    # 检测业务状态
    result = response.get(const.WXPaymentNotify.Status)

    # 支付失败
    if result != const.WXPayResponse.Success:
        payfail.notify(appid, openid, orderid, fee, **kvparas)
        return _STANDARD_REPLY

    fee = payment.currency_reverter(int(fee))
    paysuccess.notify(appid, openid, orderid, fee, **kvparas)

    return _STANDARD_REPLY
