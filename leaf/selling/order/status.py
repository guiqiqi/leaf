"""订单的所有状态"""

from typing import NoReturn, Dict
from ...core.algorithm import fsm

from . import events
from .settings import Status as settings

# 状态 - 订单已经创建
Created = fsm.State(0, settings.Description.Created)
Created.add(events.Confirm)
Created.add(events.UserClose)

# 状态 - 用户开始支付
Confirmed = fsm.State(1, settings.Description.Confirmed)
Confirmed.add(events.Paying)


class _Paying(fsm.State):
    """状态 - 用户正在支付"""

    def enter(self, payments: fsm.Event):
        """进入正在支付状态 - 保存支付详情"""
        self.extra = payments.extra


Paying = _Paying(2, settings.Description.Paying)
Paying.add(events.PayingSuccess)
Paying.add(events.PayingFailed)


class _Paid(fsm.State):
    """状态 - 订单支付成功"""

    def enter(self, payid: fsm.Event):
        """进入支付成功状态 - 保存支付单详情"""
        self.extra = payid.extra


Paid = _Paid(3, settings.Description.Paid)
Paid.add(events.Shipped)


class _PayFailed(fsm.State):
    """状态 - 用户支付失败"""

    def enter(self, reason: fsm.Event):
        """进入支付失败状态 - 保存支付失败原因"""
        self.extra = reason.extra


PayFailed = _PayFailed(4, settings.Description.PayFailed)
PayFailed.add(events.OrderRetry)
PayFailed.add(events.OrderTimedOut)


class _Shipping(fsm.State):
    """状态 - 订单正在运送"""

    def enter(self, reason: fsm.Event):
        """进入运送状态保存运单信息并创建详细信息列表"""
        self.extra = reason.extra
        self.extra[settings.ExtraInfomation.ShipDetails] = list()


Shipping = _Shipping(5, settings.Description.Shipping)
Shipping.add(events.Delieverd)


# 状态 - 订单已签收
Delieverd = fsm.State(6, settings.Description.Delieverd)
Delieverd.add(events.RecieveTimingExcced)
Delieverd.add(events.Recieved)


# 状态 - 订单完成
Completed = fsm.State(7, settings.Description.Completed)
Completed.add(events.RequestRefund)


class _RefundReviewing(fsm.State):
    """状态 - 退款正在审核"""

    def enter(self, reason: fsm.Event):
        """
        进入退款审核状态时需要采集:
            0. 退款申请原因
            1. 退款申请事件生成的退款申请码
        """
        self.extra = reason.extra


RefundReviewing = fsm.State(8, settings.Description.RefundReviewing)
RefundReviewing.add(events.RefundApproved)
RefundReviewing.add(events.RefundDenied)


Refunding = fsm.State(9, settings.Description.Refunding)
Refunding.add(events.RefundSuccess)
Refunding.add(events.RefundFailed)


class _Closed(fsm.State):
    """状态 - 订单关闭"""

    def enter(self, reason: fsm.Event):
        """
        进入订单关闭时检测进入原因:
            0. 如果是用户主动关闭则记录关闭原因
            1. 如果是发生了订单超时事件则记录为订单超时
            2. 如果是退款则记录订单已经完成退款
        """
        self.extra[settings.ExtraInfomation.OperateTime] = reason.time
        self.extra[settings.ExtraInfomation.Reason] = reason.description
        if reason == events.UserClose:
            self.extra = reason.extra


Closed = _Closed(10, settings.Description.Closed)
