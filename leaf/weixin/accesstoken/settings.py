"""
AccessToken 获取配置
"""

# 默认最大的重试次数 - 大于零
MaxRetries = 5

# 每两次获取之间的时间间隔
Pre = 30
Gap = 7200 - Pre

# 请求的地址
Address = "https://api.weixin.qq.com/cgi-bin/token"
