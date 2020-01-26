"""订单相关设置"""


class Events:
    """事件相关设置"""

    class Key:
        """导出键设置"""
        OperationCode = "code"  # 操作码
        Time = "time"  # 发生时间
        Description = "description"  # 描述
        Extra = "extra"  # 额外信息

    class ExtraInformation:
        """额外信息描述键"""
        CloseReason = "订单关闭原因"
        Payments = "支付详情"
        PayId = "支付单号"
        PayFee = "实际支付金额"
        PayFailReason = "支付失败原因"
        ShipInfo = "物流信息"
        RefundReason = "退款原因"
        RefundNumber = "退款单号"
        RefundDenyReason = "退款申请未通过原因"
        RefundFailReason = "退款在支付平台处理失败原因"

    class Description:
        """描述设置"""
        Confirm = "用户已经确认了订单, 等待支付"
        UserClose = "用户主动关闭订单"
        Paying = "用户正在付款, 等待支付结果"
        PayingSuccess = "用户已支付成功"
        PayingFailed = "用户支付失败"
        OrderRetry = "支付失败, 转入重试"
        OrderTimedOut = "订单超时, 系统关闭订单"
        Shipped = "商品已经交付物流"
        Delieverd = "商品已经送达"
        Recieved = "用户确认收货"
        RecieveTimingExcced = "超时系统自动确认收货"
        RequestRefund = "用户申请退款"
        RefundDenied = "用户退款申请已拒绝"
        RefundApproved = "用户退款申请已通过, 等待支付平台处理退款"
        RefundSuccess = "支付平台退款完成"
        RefundFailed = "支付平台退款失败"


class Status:
    """订单状态相关设置"""

    class Key:
        """导出键设置"""
        Code = "code"  # 状态码
        Description = "description"  # 说明
        Extra = "extra"  # 额外信息

    class ExtraInfomation:
        """额外信息补充描述"""
        Reason = "原因"
        Operator = "操作者"
        OperateTime = "操作时间"
        ShipDetails = "物流详细信息"

    class Description:
        """订单状态描述"""
        Created = "订单创建"
        Confirmed = "订单已经被确认, 等待用户支付"
        Paying = "用户正在支付, 等待支付结果"
        Paid = "用户支付成功, 等待发货"
        PayFailed = "用户支付失败, 尝试重新支付"
        Shipping = "订单已经交付物流运送"
        Delieverd = "订单物流已经完成"
        RefundReviewing = "退款单正在审核"
        Refunding = "退款已经交付支付平台处理"
        Completed = "订单已经完成"
        Closed = "订单已关闭"


class Manager:
    """订单状态管理器相关设置"""

    class Key:
        """导出键设置"""
        Name = "orderid" # 状态机名称 - 订单号
        CurrentStat = "current"  # 当前状态
        EventsRecorder = "events"  # 事件记录器
