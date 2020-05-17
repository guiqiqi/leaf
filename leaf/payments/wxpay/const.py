"""微信支付常量"""


class WXPayAddress:
    """微信支付地址相关常量"""
    XMLTag = "xml"  # 在 xml数据 外部包裹的xml标签
    Order = "https://api.mch.weixin.qq.com/pay/unifiedorder"
    Query = "https://api.mch.weixin.qq.com/pay/orderquery"
    Close = "https://api.mch.weixin.qq.com/pay/closeorder"
    Refund = "https://api.mch.weixin.qq.com/secapi/pay/refund"
    RefundQuery = "https://api.mch.weixin.qq.com/pay/refundquery"


class WXPaySignature:
    """微信支付签名常量"""
    class Value:
        """固定值"""
        Type = "MD5"  # 使用 MD5 方式签名
        Version = "1.0"  # 固定值 1.0

    class Key:
        """固定键"""
        ApiKey = "key"  # Apikey
        Version = "version"  # 签名版本
        Sign = "sign"  # 签名
        Type = "sign_type"  # 签名类型
        Nonce = "nonce_str"  # 随机字符


class WXPayBasic:
    """微信支付基础常量"""
    AppID = "appid"  # appid键
    Mch = "mch_id"  # 商户号键
    OpenID = "openid"  # OpenID
    TransactionID = "transaction_id"  # 微信支付交易ID


class WXPaymentNotify:
    """支付结果通知常量"""

    Status = "result_code"

    Fee = "cash_fee"  # 支付金额
    FeeType = "cash_fee_type"  # 支付币种

    class Error:
        """支付失败"""
        Code = "err_code"  # 错误代码键
        Description = "err_code_des"  # 错误描述


class WXPayResponse:
    """微信支付响应常量"""
    Status = "return_code"  # 通讯状态
    Message = "return_msg"  # 通讯消息
    Success = "SUCCESS"  # 通讯成功
    Fail = "FAIL"  # 通讯失败
    Nothing = "OK"  # 回复消息


class WXPayOrder:
    """微信支付订单常量"""
    Callback = "notify_url"  # 支付结果通知键

    class Type:
        """交易类型信息"""
        InApp = "APP"  # APP 内部
        ScanQR = "NATIVE"  # 原生支付
        JSAPI = "JSAPI"  # JSAPI 支付

    class GoodsDetail:
        """详细信息内部键"""
        Name = "goods_name"  # 商品名称
        Quantity = "quantity"  # 商品数量
        Key = "goods_detail"  # 外层包裹键

    class Info:
        """订单信息"""
        Describe = "body"  # 订单描述
        Detail = "detail"  # 详细信息
        Type = "trade_type"  # 交易类型 - JSAPI...
        Attach = "attach"  # 附加信息
        ProductID = "product_id"  # 商品id

    class Time:
        """订单时间信息"""
        Start = "time_start"  # 开始时间
        End = "time_expire"  # 过期时间
        Format = "%Y%m%d%H%M%S"  # 时间格式化模板
        Accuracy = 1000  # 时间生成器精度

    class Device:
        """支付设备信息"""
        IP = "spbill_create_ip"  # 发起支付设备IP
        ID = "device_info"  # 发起支付设备ID

    class Fee:
        """支付金额常量"""
        Amount = "total_fee"  # 订单总金额
        Currency = "fee_type"  # 订单支付币种

    class ID:
        """Id 相关常量"""
        In = "out_trade_no"  # 商户的订单 Id
        Out = "transaction_id"  # 微信的 trasaction_id
        Prepay = "prepay_id"  # jsapi 调用返回的 prepay_id


class WXPayRefund:
    """退款相关常量"""
    Offset = "offset"  # 从第几个开始查询
    CurrentRefund = "refund_count"  # 当前退款单数
    TotalRefunds = "total_refund_count"  # 总共退款单数

    class Result:
        """退款结果信息"""
        @staticmethod
        def Status(no):
            """第几单的退款状态"""
            return "refund_status_" + str(no)

        @staticmethod
        def Account(no):
            """第几单的退款去向"""
            return "refund_recv_account_" + str(no)

        @staticmethod
        def Time(no):
            """第几单的退款成功时间"""
            return "refund_success_time_" + str(no)

    class ID:
        """ID 常量"""
        In = "out_refund_no"  # 商户退款 ID
        Out = "refund_id"  # 微信退款单号

    class Fee:
        """支付金额常量"""
        Amount = "refund_fee"  # 退款金额
        Currency = "refund_fee_type"  # 退款币种
