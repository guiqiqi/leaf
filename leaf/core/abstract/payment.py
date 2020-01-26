"""Leaf 支付方式抽象类"""


class AbstractPayment:
    """支付方式的抽象类"""
    description: str = str() # 这种支付方式的名称

    def __hash__(self) -> int:
        """支付类 Hash 支持"""
        return hash(self.description)

    def __str__(self) -> str:
        """支付类描述字符串"""
        return self.description

    def pay(self, orderid: str, amount: float, duration: int, describe: str,
            currency: str, details: dict, **kwargs) -> dict:
        """支付类的调用接口 - 抽象接口
        id: str 商户订单id
        details: dict 商品详细信息
        amount: float 总价金额
        describe: str 商品描述
        currency: str 订单币种

        返回 预订单 的相关信息

        **kwargs 中可以添加自定义的一些参数
        """

    def query(self, orderid: str, **kwargs) -> dict:
        """支付类订单查询接口 - 抽象接口
        orderid: str 商户订单id/平台支付单id

        返回 当前查询订单的相关信息

        **kwargs 中可以添加自定义的一些参数
        """

    def close(self, orderid: str, **kwargs) -> dict:
        """支付累订单关闭接口 - 抽象接口
        orderid: str 商户订单id/平台支付单id

        返回关闭订单相关消息

        **kwargs 中可以添加自定义的一些参数
        """

    def refund(self, orderid: str, total_amount: float, refund_amount: float,
               refundid: str, currency: str, reason: str, **kwargs) -> dict:
        """支付类的退款接口 - 抽象接口
        orderid: str 商户订单id/平台支付单id
        amount: float 退款的金额
        refundid: str 退款id
        reason: str 退款原因
        cert: str 退款使用证书的绝对路径

        **kwargs 中可以添加自定义的一些参数
        """

    def query_refund(self, orderid: str, **kwargs) -> dict:
        """支付类的退款查询接口 - 抽象接口
        orderid: str 商户订单id/平台支付单id/商户退款单号/微信退款单号

        **kwargs 中可以添加自定义的一些参数
        """
