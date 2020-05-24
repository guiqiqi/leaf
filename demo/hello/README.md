这将是您入门 `Leaf` 使用的第一步☝️，只需要简单的环境准备与配置，您就可以在自己的微信公众号中看到一个来自 `Leaf` 的问候，让我们开始吧😄！

## 环境准备

在运行这个 `Demo` 之前，您需要按照如下步骤准备环境：

1. 安装最新版本的 `Leaf`:

   ```shell
   pip install leaf
   ```

   版本应在 `1.0.9.1.dev8` 及以上

2. 确保您当前用户有权限使用服务器的80端口

3. 在微信公众平台获取您微信公众账号的如下开发配置参数：

   - AppID
   - AppSecret
   - Token - 一般是您自己设置
   - AESEncryptKey - 如果您选择加密/混合模式发送消息

## 配置文件

之后在 `config.py` 的 第 98 - 101 行分别填入您刚刚获取到的开发参数：

```python
weixin = Static({
    "appid": "wxabcd1234abcd1234",  # AppID
    "aeskey": "s5d6t7vybotcre3465d68f7ybvtd4sd5687g8huhyvt",  # AESEncryptKey
    "token": "s547d6figobunb67568d8f7g8ohjiks1",  # Token
    "secret": "f5a3462707c2a31e51ff1b04efd1ed39",  # AppSecret
		...
})
```

## 开始

运行我们的服务器：

```shell
python3 run.py
```

所有配置都已经完成，在微信公众平台接口配置信息的 `URL` 部分填入您服务器的域名+ `/weixin/callback` 之后提交；

现在，在您的公众号发送一条消息，即可看到来自 `Leaf` 的问候！![weixin](https://github.com/guiqiqi/leaf/blob/dev/demo/hello/weixin.jpg?raw=true)

直接访问您的域名也可以看到它：

![http](https://github.com/guiqiqi/leaf/blob/dev/demo/hello/http.jpg?raw=true)

Enjoy using! 😉 

