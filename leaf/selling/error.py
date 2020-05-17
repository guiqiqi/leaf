"""销售相关错误定义"""

from ..core import error as _error


class ProductNotFound(_error.Error):
    """根据给定信息找不到对应的产品"""
    code = 10025
    description = "根据给定信息找不到对应的产品"


class ProductParameterNotFound(_error.Error):
    """找不到对应的产品参数信息"""
    code = 10026
    description = "找不到对应的产品参数信息"


class ProductParameterConflicting(_error.Error):
    """产品参数信息冲突"""
    code = 10027
    description = "产品参数信息发现重复"


class StockNotFound(_error.Error):
    """根据给定信息找不到对应商品"""
    code = 10028
    description = "根据给定信息找不到对应的商品"


class InvalidCurrency(_error.Error):
    """非允许的交易货币类型"""
    code = 10029
    description = "不允许给定的货币类型进行交易"


class EmptyOrder(_error.Error):
    """试图创建一个空订单信息"""
    code = 10030
    description = "不能用空商品列表创建订单"


class DiffrentCurrencies(_error.Error):
    """创建订单的商品货币类型不统一"""
    code = 10031
    description = "商品货币类型不统一"


class DiscontinueStock(_error.Error):
    """给定的商品已经停售"""
    code = 10032
    description = "试图创建订单的商品已经停售"


class InsufficientInventory(_error.Error):
    """库存不足"""
    code = 10033
    description = "所选商品库存不足"


class InvalidPaymentCallback(_error.Error):
    """支付平台通知到的订单信息找不到了 - 这可是很严重的错误"""
    code = 10034
    description = "无法找到支付平台通知到的订单"
