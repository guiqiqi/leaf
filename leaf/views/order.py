"""订单相关的接口与事件绑定"""

import logging
from typing import NoReturn

from flask import Blueprint

from ..core import modules
from ..core import events as _events
from ..core.error import Error as _Error

from ..selling import error
from ..selling.order import Order
from ..selling.order import events

order = Blueprint("order", __name__)

# 注册支付成功与失败及退款提醒事件
# 位置参数列表 - openid, transaction id, trade_out_no, cash_fee
logger = logging.getLogger("leaf.selling.order")


def _paysucess_handler(_openid: str, tactid: str, orderid: str, amount: float) -> NoReturn:
    """支付成功通知处理"""
    # pylint: disable=no-member
    _order = Order.objects(id=orderid)

    try:
        # 被通知到的订单不存在 - 记录错误(严重错误)
        if not _order:
            raise error.InvalidPaymentCallback(
                orderid + ' - ' + str(amount))
        _order: Order = _order.pop()

        # 生成一个支付成功的有限状态机事件
        paid = events.PayingSuccess()
        paid.action(tactid, amount)
        _order.manager.handle(paid)

    except _Error as _error:
        logger.exception(_error)


def _payfail_handler(_openid: str, tactid: str, orderid: str,
                     amount: float, reason: str) -> NoReturn:
    """支付失败通知处理"""
    # pylint: disable=no-member
    _order = Order.objects(id=orderid)

    try:
        # 被通知到的订单不存在 - 记录错误(严重错误)
        if not _order:
            raise error.InvalidPaymentCallback(
                orderid + ' - ' + str(amount))
        _order: Order = _order.pop()

        # 生成一个支付失败的有限状态机事件
        payfailed = events.PayingFailed()
        payfailed.action(tactid, reason)
        _order.manager.handle(payfailed)

    except _Error as _error:
        logger.exception(_error)


_wxpay_paysuccess: _events.Event = modules.events.event(
    "leaf.payments.wxpay.notify.pay.success")
_wxpay_payfail: _events.Event = modules.events.event(
    "leaf.payments.wxpay.notify.pay.fail")

_wxpay_paysuccess.hook(_paysucess_handler)
_wxpay_payfail.hook(_payfail_handler)
# _wxpay_refund.hook()  # 暂时不启用
