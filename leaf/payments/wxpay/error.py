"""微信支付错误类定义"""

from ...core.error import Error


class WXPayError(Error):
    """微信支付错误"""
    code = 19000
    description = "微信支付错误父类"


class WXPaySignatureError(WXPayError):
    """微信支付签名错误"""
    code = 19001
    description = "签名验证错误 - 警惕端口扫描"
