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
