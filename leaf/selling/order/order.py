"""订单类数据库模型"""

import pickle
import logging
from typing import List, NoReturn
import mongoengine

from . import manager as _man
from . import events
from .. import error
from .. import settings
from ..commodity import stock
from ...core import modules
from ...core import schedule
from ...core.error import Error as _Error
from ...core.algorithm import fsm
from ...views import wxpay as _wxpay


# 注册支付成功与失败及退款提醒事件
# 位置参数列表 - openid, transaction id, trade_out_no, cash_fee
logger = logging.getLogger("leaf.selling.order")


def _paysucess_handler(_openid: str, tactid: str, orderid: str, amount: float) -> NoReturn:
    """支付成功通知处理"""
    # pylint: disable=no-member
    order = Order.objects(id=orderid)

    try:
        # 被通知到的订单不存在 - 记录错误(严重错误)
        if not order:
            raise error.InvalidPaymentCallback(
                orderid + ' - ' + str(amount))
        order: Order = order.pop()

        # 生成一个支付成功的有限状态机事件
        paid = events.PayingSuccess()
        paid.action(tactid, amount)
        order.manager.handle(paid)

    except _Error as _error:
        logger.exception(_error)


def _payfail_handler(_openid: str, tactid: str, orderid: str,
                     amount: float, reason: str) -> NoReturn:
    """支付失败通知处理"""
    # pylint: disable=no-member
    order = Order.objects(id=orderid)

    try:
        # 被通知到的订单不存在 - 记录错误(严重错误)
        if not order:
            raise error.InvalidPaymentCallback(
                orderid + ' - ' + str(amount))
        order: Order = order.pop()

        # 生成一个支付失败的有限状态机事件
        payfailed = events.PayingFailed()
        payfailed.action(tactid, reason)
        order.manager.handle(payfailed)

    except _Error as _error:
        logger.exception(_error)


_wxpay.paysuccess.hook(_paysucess_handler)
_wxpay.payfail.hook(_payfail_handler)
# _wxpay.refund.hook()  # 暂时不启用


class Order(mongoengine.Document):
    """
    订单类数据库模型:
        amount: 订单总金额 - float
        goods: 购买商品列表 - List[CacheedRef]
        status: 当前状态JSON字串 - str
        instance: 订单状态管理器的 pickle 对象 - bytes
    """
    amount = mongoengine.FloatField(min_value=0, required=True)
    currency = mongoengine.StringField(
        default=settings.General.DefaultCurrency)

    goods = mongoengine.ListField(
        mongoengine.CachedReferenceField(stock.Stock))
    instance = mongoengine.BinaryField(default=bytes)

    @staticmethod
    def create(goods: List[stock.Stock],
               timeout: int = settings.Order.OrderTimeout) -> Order:
        """根据给定的商品列表创建一个订单类实例后入库"""

        # 检查列表是否为空
        if not goods:
            raise error.EmptyOrder(str(goods))

        # 检查商品是否都在售
        for good in goods:
            if not good.onsale:
                raise error.DiscontinueStock(good.id)

        # 检查商品设置的货币类型是否相同
        currencies = [good.currency for good in goods]
        if len(set(currencies)) != 1:
            raise error.DiffrentCurrencies(str(currencies))

        # 检查商品是否还有库存
        inventories = [good.inventory for good in goods]
        if not min(inventories):
            _iid = goods[inventories.index(0)].id
            raise error.InsufficientInventory(_iid)

        # 目标对象库存减少一
        for good in goods:
            good.inventory -= 1
            good.save()

        currency = currencies.pop()
        amount = sum([good.price for good in goods])
        order = Order(amount=amount, currency=currency, goods=goods)
        order.save()

        # pylint: disable=no-member
        instance = _man.StatusManager(order.id)
        instance.start()
        order.instance = pickle.dumps(instance)

        # 设置订单超时定时器
        def __cancel_order():
            """取消当前订单"""
            cancellation = events.OrderTimedOut()
            order.manager.handle(cancellation)
        timer = schedule.Worker(__cancel_order, timeout, 1)
        schedule_manager: schedule.Manager = modules.schedules
        schedule_manager.start(timer)

        return order.save()

    @property
    def manager(self):
        """返回当前订单类的 manager 实例代理"""
        if not self.instance:
            return None
        man: _man.StatusManager = pickle.loads(self.instance)
        return ManagerProxy(self, man)


class ManagerProxy:
    """
    代理Manager的访问
    add 函数不代理 - 实例化后的状态机不应该改变状态图
    """

    def __init__(self, db: Order, instance: _man.StatusManager):
        """实例化代理对象"""
        self._db, self._instance = db, instance

    def json(self):
        """代理 json 提取操作"""
        return self._instance.json()

    @property
    def name(self) -> str:
        """返回名称"""
        return self._instance.name

    @property
    def current(self) -> fsm.State:
        """返回当前状态"""
        return self._instance.current

    @property
    def events(self) -> List[fsm.Event]:
        """代理 events 操作"""
        return self._instance.events

    def stop(self) -> NoReturn:
        """代理 stop 操作"""
        self._instance.stop()
        self._db.instance = pickle.dumps(self._instance)
        self._db.save()

    def start(self) -> NoReturn:
        """代理 start 操作"""
        self._instance.start()
        self._db.instance = pickle.dumps(self._instance)
        self._db.save()

    def handle(self, event: fsm.Event) -> NoReturn:
        """代理事件处理操作"""
        self._instance.handle(event)
        self._db.instance = pickle.dumps(self._instance)
        self._db.save()
