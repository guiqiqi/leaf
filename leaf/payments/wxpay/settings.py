"""微信支付设置量"""


class Order:
    """订单相关设置"""
    DefaultCurrency = "CNY"  # 默认货币为人民币
    MoreAttr = " ..."  # 当多个商品时添加的说明
    PaymentDescription = "微信支付" # 支付方式的名称


class NetworkAndEncrypt:
    """网络与加密相关设置"""
    NonceLength = 32  # 随机字符串不长于 32 位
    ExternalIPProvider = "https://api.ipify.org"  # 外部IP地址提供


class PaymentNotify:
    """支付结果通知中相关设置"""

    # 需要从结果中提取的业务相关键
    Keys = {
        "mch_id": "mchid",
        "is_subscribe": "subcribe",
        "bank_type": "bank",
        "time_end": "endtime",
        "transaction_id": "transaction",
        "attach": "attach"
    }
