"""
使用有限状态机算法
通过已经创建的事件和状态
对订单状态进行自动的调度
"""
# pylint: disable=arguments-differ

from typing import NoReturn
from ...core.tools import web
from ...core.algorithm import fsm

from . import events
from . import status
from . import settings

# 状态转移表
_TransferTable = (
    (status.Created, events.Confirm, status.Confirmed),
    (status.Created, events.UserClose, status.Closed),
    (status.Confirmed, events.Paying, status.Paying),
    (status.Paying, events.PayingSuccess, status.Paid),
    (status.Paying, events.PayingFailed, status.PayFailed),
    (status.PayFailed, events.OrderTimedOut, status.Closed),
    (status.PayFailed, events.OrderRetry, status.Created),
    (status.Paid, events.Shipped, status.Shipping),
    (status.Shipping, events.Delieverd, status.Delieverd),
    (status.Delieverd, events.Recieved, status.Completed),
    (status.Delieverd, events.RecieveTimingExcced, status.Completed),
    (status.Completed, events.RequestRefund, status.RefundReviewing),
    (status.RefundReviewing, events.RefundApproved, status.Refunding),
    (status.RefundReviewing, events.RefundDenied, status.Completed),
    (status.Refunding, events.RefundSuccess, status.Closed),
    (status.Refunding, events.RefundFailed, status.Completed)
)


class StatusManager(fsm.Machine):
    """创建一个订单状态管理器"""

    def __init__(self, orderid: str) -> NoReturn:
        """
        订单状态管理器构造函数:
            0. 根据订单id对管理器命名
            1. 初始化状态转移对应表
            2. 初始化进入状态
        """
        super().__init__(str(orderid))

        # 初始化状态转移对应表
        for record in _TransferTable:
            self.add(*record)

    def start(self) -> NoReturn:
        """开始从订单创建开始"""
        super().start(status.Created)

    def json(self) -> str:
        """将当前状态信息导出为 JSON 字串"""
        if not self.current is None:
            current = {
                settings.Status.Key.Code: self.current.code,
                settings.Status.Key.Description: self.current.description,
                settings.Status.Key.Extra: self.current.extra
            }  # 当前状态导出字典
        else:
            current = None

        mapping = map(lambda event: {
            settings.Events.Key.Time: event.time,
            settings.Events.Key.OperationCode: event.opcode,
            settings.Events.Key.Extra: event.extra,
            settings.Events.Key.Description: event.description
        }, self.events)  # 事件记录器导出为字典

        return web.JSONcreater({
            settings.Manager.Key.Name: self.name,
            settings.Manager.Key.CurrentStat: current,
            settings.Manager.Key.EventsRecorder: list(mapping)
        })
