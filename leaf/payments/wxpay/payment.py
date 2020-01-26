"""微信支付模块主文件"""

from socket import gethostname
from functools import lru_cache
from typing import Tuple, Dict, Callable, Optional, NoReturn

from ...core.tools import web, time
from ...core.abstract import payment

from . import const
from . import settings
from . import signature


class WXPayment(payment.AbstractPayment):
    """微信支付类"""
    description = settings.Order.PaymentDescription

    @staticmethod
    def _productid_selector(details: dict) -> str:
        """从传入的商品信息中选择数量最多的那一个的ID"""

        # 如果传入的是空的
        if not details:
            return str()

        # 首先交换 {good: number: int}
        exchanged = dict(zip(details.values(), details.keys()))

        # 之后选择数量最多的键
        maxgood = exchanged[max(exchanged)]

        # 返回商品 ID
        return str(maxgood.id)

    @staticmethod
    def _details_converter(details: dict) -> str:
        """
        将传入的字典数据转换成微信支付平台标准格式:
        {
            str(商品) = 商品名: 数量,
            ...
        }
            ->
        "{
            goods_detail:{
                "goods_name": str(商品),
                "quantity": int
            },
            ...
        }"
        """
        # 如果传入的是空字典
        if not details:
            return str()

        # 通过遍历商品列表进行转换
        goods = list()
        converted = {const.WXPayOrder.GoodsDetail.Key: goods}
        for good, quantity in details.items():
            formatted = {
                const.WXPayOrder.GoodsDetail.Name: str(good),
                const.WXPayOrder.GoodsDetail.Quantity: quantity
            }
            goods.append(formatted)

        # 返回 JSON 格式数据
        return web.JSONcreater(converted)

    @staticmethod
    def currency_converter(amount: float) -> int:
        """将人民币元转化成分并四舍五入"""
        return int(amount * 100)

    @staticmethod
    def currency_reverter(amount: int) -> float:
        """将微信整数价格转为人民币"""
        return float(amount) / 100

    @staticmethod
    @lru_cache()
    def _external_ip() -> str:
        """返回的值确定机器外部IP地址"""
        httpresult = web.get(settings.NetworkAndEncrypt.ExternalIPProvider)
        return httpresult.data

    @staticmethod
    def _machine_name() -> str:
        """获取当前发送支付请求的设备名称"""
        return gethostname()

    @staticmethod
    def _calculate_time(duration: int) -> Tuple[str, str]:
        """
        计算订单的生成时间, 并根据传入的有效时间计算:
        订单的结束时间, 并将其转化为微信的格式, 之后将两个值一起返回
        *duration:int - 以秒为单位的时间间隔
        """
        now = time.now()
        end = now + duration
        startstr = time.timestr(now, const.WXPayOrder.Time.Format)
        endstr = time.timestr(end, const.WXPayOrder.Time.Format)
        return startstr, endstr

    def __repr__(self) -> str:
        """返回 repr 信息"""
        return "<Leaf Payments.WXPayment with appid: %s>" % self.__appid

    def __init__(self, appid: str, mchid: str, apikey: str,
                 callbacks: Dict[str, str],
                 cert: Tuple[str, str],
                 ordertype: Callable[[dict], NoReturn]):
        """
        WXPayment 类构造函数
        appid: 公众平台 APPID
        apikey: API 密钥
        mchid: 商户 ID
        cert: (签名文件地址, 密钥文件地址)
        callbacks: {支付类功能函数名: 回调地址}
        ordertype: 订单类型 - wxpay.methods 中的任一静态函数
        """
        # 保存类信息
        self.__cert: tuple = cert
        self.__appid = appid
        self.__mchid = mchid
        self.__apikey = apikey
        self.__ordertype = ordertype
        self.__callbacks = callbacks

        # 生成签名工具实例
        self.__signature = signature.SignatureTool(apikey)

    def request(self, unsigned, address,
                cert: Optional[bool] = False,
                args: Optional[Tuple[str]] = None) -> dict:
        """
        向微信的支付后端发起支付请求:
            unsigned: 未经过签名的业务数据包
            address: 微信的相关支付 API 地址
            cert: 是否使用微信提供的证书文件连接
            *args: 需要从中提取的数据键

        *注意: 当 args 中的数据键在 response 中不存在时不会引起错误
        """
        # 将请求签名之后编码发送
        self.__signature.do(unsigned)
        signed = unsigned
        xmldata = web.XMLcreater({const.WXPayAddress.XMLTag: signed}, False)

        # 根据要求判断是否使用证书连接
        if cert is True:
            response, connection = web.post(
                address, None, xmldata, None, self.__cert)
        else:
            response, connection = web.post(address, None, xmldata)

        # 解编码响应并关闭连接
        response = web.XMLparser(response)
        response = response.get(const.WXPayAddress.XMLTag, {})
        connection.close()

        # 如果没有需要的信息 - 直接返回所有业务数据
        if not args:
            return response

        # 如果有需要的信息 - 提取需要的键值对
        result = dict()
        for needkey in args:
            if needkey in response.keys():
                result[needkey] = response[needkey]
        return result

    def pay(self, orderid: str, amount: float,
            duration: int, describe: str, currency: str,
            details: Optional[Dict] = None, **kwargs) -> dict:
        """
        微信支付类 - 统一下单接口:
        kwargs 中的 attachment 和 openid 将会被采用

        *注意: duration 对应支付单的有效期限(秒为单位)
        *注意: 当使用 JSAPI 支付时需要主动传入 Openid
        *注意: 传入的 detials 格式:
            {"商品名" / 支持 str(商品)=商品名类: 数量}
        """
        # 获取订单时间
        start, end = self._calculate_time(duration)

        # 获取补充信息
        attachment = kwargs.get("attachment", str())
        openid = kwargs.get("openid", str())

        # 创建订单
        order: dict = {
            # 添加微信支付平台基础信息
            const.WXPayBasic.AppID: self.__appid,
            const.WXPayBasic.Mch: self.__mchid,
            const.WXPayBasic.OpenID: openid,

            # 添加设备基础信息
            const.WXPayOrder.Device.IP: self._external_ip(),
            const.WXPayOrder.Device.ID: self._machine_name(),

            # 添加订单信息
            const.WXPayOrder.ID.In: orderid,
            const.WXPayOrder.Fee.Amount: self.currency_converter(amount),
            const.WXPayOrder.Fee.Currency: currency,

            # 添加订单商品信息
            const.WXPayOrder.Info.Describe: describe,
            const.WXPayOrder.Info.ProductID: self._productid_selector(details),

            # 添加商品时间戳
            const.WXPayOrder.Time.Start: start,
            const.WXPayOrder.Time.End: end,

            # 添加自定义信息
            const.WXPayOrder.Callback: self.__callbacks.get("pay"),
            const.WXPayOrder.Info.Attach: attachment
        }

        # 为订单指定支付方式
        self.__ordertype(order)

        # 获取回传信息
        response = self.request(order, const.WXPayAddress.Order)
        return response

    def query(self, orderid: str, **kwargs) -> dict:
        """
        微信支付类 - 订单查询接口实现
        *orderid: 统一为商户内部订单 id
        """
        request = dict({
            # 添加微信支付平台基础信息
            const.WXPayBasic.AppID: self.__appid,
            const.WXPayBasic.Mch: self.__mchid,

            # 添加订单信息
            const.WXPayOrder.ID.In: orderid
        })

        # 获取回传信息
        response = self.request(request, const.WXPayAddress.Query)
        return response

    def close(self, orderid: str, **kwargs) -> dict:
        """
        微信支付类 - 关闭订单接口实现
        *orderid: 统一为商户内部订单 id
        """
        request = dict({
            # 添加微信平台基础信息
            const.WXPayBasic.AppID: self.__appid,
            const.WXPayBasic.Mch: self.__mchid,

            # 添加订单信息
            const.WXPayOrder.ID.In: orderid
        })

        # 获取回传信息
        response = self.request(request, const.WXPayAddress.Close)
        return response

    def refund(self, orderid: str, total_amount: float,
               refund_amount: float, refundid: str,
               currency: str, reason: str, **kwargs) -> dict:
        """
        微信支付类 - 退款申请接口:
            orderid: 对应的订单id
            total_amount: 订单总金额
            refund_amount: 退款金额
            refundid: 商户内部的唯一退款id
            currency: 币种
            reason: 退款原因
        """
        request = dict({
            # 添加微信平台基础信息
            const.WXPayBasic.AppID: self.__appid,
            const.WXPayBasic.Mch: self.__mchid,

            # 添加订单信息
            const.WXPayOrder.ID.In: orderid,
            const.WXPayOrder.Fee.Amount: self.currency_converter(total_amount),

            # 添加退款信息
            const.WXPayRefund.ID.In: refundid,
            const.WXPayRefund.Fee.Amount: self.currency_converter(refund_amount),
            const.WXPayRefund.Fee.Currency: currency,

            # 添加回调信息
            const.WXPayOrder.Callback: self.__callbacks.get("refund")
        })

        # 获取返回信息
        response = self.request(
            request, const.WXPayAddress.Refund, True)
        return response

    def query_refund(self, orderid: str, **kwargs) -> dict:
        """
        微信支付类 - 退款查询接口:
            orderid: 商户内部统一订单id

        *注意: 如果需要指定查询某一单的退款信息,
        请在 kwargs 中指定 offset = n
        """
        offset = str(kwargs.get("offset", 1))

        request = dict({
            # 添加微信平台基础信息
            const.WXPayBasic.AppID: self.__appid,
            const.WXPayBasic.Mch: self.__mchid,

            # 添加退款单/订单信息
            const.WXPayOrder.ID.In: orderid,
            const.WXPayRefund.Offset: offset
        })

        # 获取回传信息
        response = self.request(request, const.WXPayAddress.RefundQuery)
        return response
