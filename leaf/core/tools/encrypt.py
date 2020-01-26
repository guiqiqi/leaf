"""加密常用的工具包"""

import hmac
import html
import uuid
import zlib
import string
import socket
import struct
import base64
import hashlib

import random as random_module
from typing import Iterable, Optional
from Crypto.Cipher import AES

_AES_MODE = AES.MODE_CBC  # 默认的AES加密模式
_BLOCK_SIZE = 32  # 默认补位区块大小


class EncryptTools:
    """一些加密过程需要的工具"""

    @staticmethod
    def uuid() -> str:
        """生成一个UUID"""
        return uuid.uuid1().hex

    @staticmethod
    def packer(text: str) -> bytes:
        """通过给定字符串计算网络字节补位"""
        network_long = socket.htonl(len(text))
        packed = struct.pack("I", network_long)
        return packed

    @staticmethod
    def unpacker(text: bytes) -> str:
        """通过给定字符串删除网络字节补位"""
        unpacked_length = struct.unpack("I", text[:4])[0]
        unpacked = text[4:unpacked_length + 4]
        return unpacked

    @staticmethod
    def base64encode(text: bytes) -> bytes:
        """base64编码函数"""
        encoded = base64.b64encode(text)
        return encoded

    @staticmethod
    def base64decode(encoded: bytes) -> bytes:
        """base64解码函数"""
        decoded = base64.b64decode(encoded, None)
        return decoded

    @staticmethod
    def htmlencode(unescaped: str) -> str:
        """将传入字符串进行HTML编码"""
        escaped = html.escape(unescaped, False)
        return escaped

    @staticmethod
    def htmldecode(escaped: str) -> str:
        """将传入字符串进行HTML编码"""
        unescaped = html.unescape(escaped)
        return unescaped

    @staticmethod
    def PKCS7encode(text: bytes, block_size: int = _BLOCK_SIZE) -> bytes:
        """提供通过PKCS7算法编码方法"""
        length = len(text)
        pad_amount = block_size - (length % block_size)
        if pad_amount == 0:
            pad_amount = block_size
        pad = chr(pad_amount)
        treated = text + (pad * pad_amount).encode()
        return treated

    @staticmethod
    def PKCS7decode(text: bytes) -> bytes:
        """提供通过PKCS7算法解码方法"""
        pad = ord(text[-1:])
        if pad < 1 or pad > 32:
            pad = 0
        origin = text[:-pad]
        return origin

    @staticmethod
    def AESencrypt(clear: bytes, key: bytes, mode: int = _AES_MODE) -> bytes:
        """
        AES加密方法

        * 这里的明文需要已经进行过补位计算
        """
        cryptor = AES.new(key, mode, key[:16])

        # 截取key的倒数16位作为初始化向量
        cipher = cryptor.encrypt(clear)
        return cipher

    @staticmethod
    def AESdecrypt(cipher: bytes, key: bytes, mode=_AES_MODE) -> bytes:
        """
        AES解密方法

        * 这里的密文需要已经用base64解码
        """
        cryptor = AES.new(key, mode, key[:16])

        # 截取key的倒数16位作为初始化向量
        clear = cryptor.decrypt(cipher)
        return clear

    @staticmethod
    def HMAC_SHA1(clear: bytes, key: bytes) -> str:
        """使用HMAC-SHA1进行对称加密"""
        signature = hmac.new(key, msg=clear, digestmod=hashlib.sha1)
        return signature.hexdigest()

    @staticmethod
    def HMAC_SHA256(clear: bytes, key: bytes) -> str:
        """使用HMAC-SHA256进行对称加密"""
        signature = hmac.new(key, msg=clear, digestmod=hashlib.sha256)
        return signature.hexdigest()

    @staticmethod
    def SHA1(clear: str) -> str:
        """使用SHA1算法对传入消息进行摘要计算"""
        SHA1 = hashlib.sha1()
        clear = clear.encode()
        SHA1.update(clear)
        cipher = SHA1.hexdigest()
        return cipher

    @staticmethod
    def SHA256(clear: str) -> str:
        """使用SHA256算法对传入消息进行摘要计算"""
        SHA256 = hashlib.sha1()
        clear = clear.encode()
        SHA256.update(clear)
        cipher = SHA256.hexdigest()
        return cipher

    @staticmethod
    def MD5(clear: str) -> str:
        """使用MD5算法对传入消息进行摘要计算"""
        MD5 = hashlib.md5()
        clear = clear.encode()
        MD5.update(clear)
        cipher = MD5.hexdigest()
        return cipher

    @staticmethod
    def CRC32(clear: str) -> str:
        """使用CRC32算法对传入消息进行摘要计算"""
        clear = clear.encode()
        cipher = zlib.crc32(clear)
        return cipher

    @staticmethod
    def random(length: int, form: Optional[Iterable] = None) -> str:
        """获取指定位数的随机字符串"""
        if form is None:
            form = string.printable.strip()
            form.replace("&\\", "")

        # 对于 Python3X 之后的版本直接调用
        if "choices" in dir(random_module):
            random_string = "".join(random_module.choices(
                form, k=length))

        # 否则自己生成一个随机列
        else:
            random_string = list()
            for _i in range(length):
                char = random_module.choice(form)
                random_string.append(char)
            random_string = "".join(random_string)
        return random_string

    @staticmethod
    def randint(start: int, end: int) -> int:
        """获取指定范围随机数"""
        return random_module.randint(start, end)
