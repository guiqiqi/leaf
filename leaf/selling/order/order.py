"""订单类数据库模型"""

import pickle
from typing import List, NoReturn
import mongoengine

from . import events
from . import manager as _man
from .. import error
from .. import settings
from ..commodity import stock

from ...core import modules
from ...core import schedule
from ...core.algorithm import fsm


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
               timeout: int = settings.Order.OrderTimeout):
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
        order.save()

        # 设置订单超时定时器
        def __cancel_order():
            """取消当前订单"""
            cancellation = events.OrderTimedOut()
            order.manager.handle(cancellation)
        timer = schedule.Worker(__cancel_order, timeout, 1, False)
        schedule_manager: schedule.Manager = modules.schedules
        schedule_manager.start(timer)
        return order

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
