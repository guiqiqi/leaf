"""微信公众平台消息加解密支持"""

from ..core.tools import encrypt
from . import const


class Encrypt:
    """
    为微信公众平台封装的消息加解密类
    """
    def __repr__(self) -> str:
        """返回 repr 信息"""
        return "<Leaf WeiXin.Encrypt>"

    def __init__(self, aeskey: str, appid: str, token: str):
        """
        加解密类构造函数:
            aeskey: 公众平台提供的 AESEncodingKey
            appid: 用户的 AppID
            token: 用户的 Token
        *注意: 这里的 Token 和 AccessToken 不是一个东西
        """
        # 公众平台提供的 AESEncodingKey 需要加上 = 之后进行 base64encode 使用
        self.__aeskey = encrypt.base64decode(aeskey + '=')

        # 保存 appid 和 token
        self.__appid = appid
        self.__token = token

    def encrypt(self, clear: str) -> str:
        """
        加密函数 - 返回加密过后的密文
        clear - 未加密的明文:
            1. 生成 16 位的随机 ASCII 字符串作为补位 -> rand = 16 bytes
            2. 计算网络字节补位 b'x00x00x00x??' -> pad  =  4 bytes
            3. 计算 rand + pad + clear.encode() + appid.encode() -> msg
            4. 对 msg PKCS7 补码(32 位补码) -> aligned = 32 * n bytes
            5. 对 aligned 使用 self.__key 进行 AES.CBC 模式加密 -> cipher
            6. 对 cipher 再一次进行 base64 编码

        *注意: 这里的明文指的是未经加密的XML全部字符串
        """
        # 准备加密需要的信息
        randstr: bytes = encrypt.random(const.Encrypt.PadLength).encode()
        pad: bytes = encrypt.packer(clear)
        msg: bytes = randstr + pad + clear.encode() + self.__appid.encode()
        aligned: bytes = encrypt.PKCS7encode(msg)

        # 进行 AES 加密
        cipher: bytes = encrypt.AESencrypt(aligned, self.__aeskey)
        cipher: bytes = encrypt.base64encode(cipher)

        return cipher.decode()

    def decrypt(self, cipher: bytes) -> str:
        """
        解密函数 - 返回解密后的明文
        按照 encrypt 加密函数倒序来一遍
        """
        # 按照顺序解密
        decoded: bytes = encrypt.base64decode(cipher)
        clear: bytes = encrypt.AESdecrypt(decoded, self.__aeskey)
        clear: bytes = encrypt.PKCS7decode(clear)

        # 前 16 为为随机字符串 - 取 16 位之后的信息
        content: bytes = clear[16:]

        # 去除 4bytes 的网络字节补位
        content = encrypt.unpacker(content)

        # 去除后 18 位的 APPID
        clear = content[0: -18]

        return clear.decode()

    def signature(self, message: str, timestamp: str, nonce: str) -> str:
        """
        根据密文计算消息体签名:
            1. 对 token, timestamp, nonce, msg_encrypted 进行排序
            2. 排序之后进行字符串拼接
            3. 返回拼接过后字符串的 SHA1 值
        """
        calculation = [message, timestamp, nonce, self.__token]
        calculation.sort()

        combined: str = ''.join(calculation)
        siganture: str = encrypt.SHA1(combined)

        return siganture
