"""
AccessToken 获取插件配置
"""

# 从公众平台拿到的 ID, Secret
AppID = "wxf23c9dc81a06ea88"
AppSecret = "f5a3462707c2a31e51ff1b04efd1ed39"

# 最大的重试次数 - 大于零
MaxRetries = 5

# 每两次获取之间的时间间隔
Gap = 7200 - 30

# 请求的地址
Address = "https://api.weixin.qq.com/cgi-bin/token"
