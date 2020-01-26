"""
常用函数工具库封装:
    web - 网络功能库
    encrypt - 加密功能库
    file - 文件功能库
    time - 时间功能库
"""

from . import web
from . import time
from . import file
from . import encrypt

web = web.WebTools
time = time.TimeTools
file = file.FileTools
encrypt = encrypt.EncryptTools
