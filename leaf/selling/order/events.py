"""所有的订单状态事件"""
# pylint: disable=arguments-differ

from typing import NoReturn, Dict

from ...core.tools import encrypt
from ...core.abstract import payment
from ...core.algorithm import fsm

from .settings import Events as settings


class Confirm(fsm.Event):
    """用户确认订单"""
    description: str = settings.Description.Confirm


class UserClose(fsm.Event):
    """用户主动关闭订单"""
    description: str = settings.Description.UserClose

    def action(self, reason: str) -> NoReturn:
        """记录用户主动关闭订单的原因"""
        self.append(settings.ExtraInformation.CloseReason, reason)


class Paying(fsm.Event):
    """用户正在付款"""
    description: str = settings.Description.Paying

    def action(self, payments: Dict[payment.AbstractPayment, float]) -> NoReturn:
        """用户支付的支付方式以及金额进行保存"""

        items: Dict[str, float] = dict()  # 支付的详情信息存储
        for method, fee in payments.items():
            items[str(method)] = fee

        self.append(settings.ExtraInformation.Payments, items)


class PayingSuccess(fsm.Event):
    """支付平台通知支付成功"""
    description: str = settings.Description.PayingSuccess

    def action(self, payid: str, fee: float) -> NoReturn:
        """记录支付单的id"""
        self.append(settings.ExtraInformation.PayId, payid)
        self.append(settings.ExtraInformation.PayFee, fee)


class PayingFailed(fsm.Event):
    """支付平台通知支付失败"""
    description: str = settings.Description.PayingFailed

    def action(self, payid: str, reason: str) -> NoReturn:
        """记录支付失败的原因"""
        self.append(settings.ExtraInformation.PayId, payid)
        self.append(settings.ExtraInformation.PayFailReason, reason)


class OrderRetry(fsm.Event):
    """订单重试"""
    description: str = settings.Description.OrderRetry


class OrderTimedOut(fsm.Event):
    """订单超时, 系统关闭订单"""
    description: str = settings.Description.OrderTimedOut


class Shipped(fsm.Event):
    """商品已经交付快递"""
    description: str = settings.Description.Shipped

    def action(self, shipping) -> NoReturn:
        """记录物流单号"""
        self.append(settings.ExtraInformation.ShipInfo, shipping)


class Delieverd(fsm.Event):
    """收到物流平台消息商品已经被送达"""
    description: str = settings.Description.Delieverd


class Recieved(fsm.Event):
    """用户主动确认收货"""
    description: str = settings.Description.Recieved


class RecieveTimingExcced(fsm.Event):
    """超时系统自动确认收货"""
    description: str = settings.Description.RecieveTimingExcced


class RequestRefund(fsm.Event):
    """用户申请退款"""
    description: str = settings.Description.RequestRefund

    def action(self, reason: str) -> NoReturn:
        """记录用户申请退款的原因并下发申请单号"""
        refundid = encrypt.uuid()
        self.append(settings.ExtraInformation.RefundReason, reason)
        self.append(settings.ExtraInformation.RefundNumber, refundid)


class RefundDenied(fsm.Event):
    """退款审核未通过"""
    description: str = settings.Description.RefundDenied

    def action(self, reason: str) -> NoReturn:
        """记录退款审核未通过的原因"""
        self.append(settings.ExtraInformation.RefundDenyReason, reason)


class RefundApproved(fsm.Event):
    """退款审核已经通过, 等待支付平台处理退款"""
    description: str = settings.Description.RefundApproved


class RefundSuccess(fsm.Event):
    """退款已经完成"""
    description: str = settings.Description.RefundSuccess


class RefundFailed(fsm.Event):
    """退款失败"""
    description: str = settings.Description.RefundFailed

    def action(self, reason: str) -> NoReturn:
        """记录退款失败信息"""
        self.append(settings.ExtraInformation.RefundFailReason, reason)
