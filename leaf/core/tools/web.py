"""常用网络函数库封装"""


import json
import uuid
import http
import gzip
import zlib
import os.path
import urllib.parse as urlparse
import urllib.request as request
from collections import namedtuple
import xml.etree.cElementTree as et

from typing import Tuple, Dict, Optional, Union

from . import file
from ..algorithm import Tree

CHROME_HEADER = {
    "Accept-Encoding":
    "deflate, gzip",
    "Accept-Language":
    "zh-CN,zh;q=0.8,en;q=0.6",
    "Cache-Control":
    "no-cache",
    "Connection":
    "Keep-Alive",
    "Pragma":
    "no-cache",
    "Accept": ("text/html,application/xhtml+xml"
               ",application/xml;q=0.9,image/webp,*/*;q=0.8"),
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/76.0.3809.100 Safari/537.36"
    )
}  # 默认的请求Header

_DEFAULT_XML_ENCODING = "utf8"  # 默认 XML 编码
_DEFAULT_XML_ROOT_NAME = "xml"  # 默认 XML ROOT 节点名称

_DECOMPRESS = "Content-Encoding"  # 获取压缩方式键
_CHARSET = "Content-Type"  # 获取 Charset 键
_DEFAULT_CHARSET = "utf-8"  # 默认网页编码

# 仅含有字节流时的 HTTP-Content 头


def _TEXT_HEADER():
    return {'Content-Type': "text/plain"}

# 仅含有表单格式的 HTTP-Content 头


def _PARAMS_HEADER():
    return {'Content-Type': 'application/x-www-form-urlencoded'}

# 文件数据混编时的 HTTP-Content 头


def _FILE_HEADER(boundry):
    return {'Content-Type': 'multipart/form-data; boundary=' + boundry}


# 生成 Web GET/POST 请求之后获取的信息类
WebResult: object = namedtuple("WebResult", ("data", "response"))


class WebTools:
    """一些网络交互过程需要的工具"""

    @staticmethod
    def urlencode(raw_url: str) -> str:
        """将网址按照 Unicode 编码"""
        encoded_url = request.quote(raw_url)
        return encoded_url

    @staticmethod
    def urldecode(encoded_url: str) -> str:
        """将网址按照 Unicode 解码"""
        raw_url = request.unquote(encoded_url)
        return raw_url

    @staticmethod
    def JSONparser(json_: str) -> dict:
        """根据JSON字符创创建字典"""
        data = json.loads(json_)
        return data

    @staticmethod
    def JSONcreater(data: dict) -> str:
        """根据字典创建JSON字符串"""

        # ensure_ascii = False - 不检查 ascii 转换错误
        json_string = json.dumps(data, ensure_ascii=False)
        return json_string

    @staticmethod
    def XMLparser(xmlstr: str) -> dict:
        """根据XML字符创创建字典"""

        # 创建 xmlTree 对象解析节点信息
        xmltree = et.fromstring(xmlstr)

        # 将 xmlTree 对象转换为内部 tree 对象
        # 这里仅仅记载 xml 中 text 的内容
        # 标签中 attribute 的部分将被丢弃
        root = Tree.fromxml(xmltree, True, False)
        itree = Tree(root)

        return itree.todict()

    @staticmethod
    def XMLcreater(data: dict, encoding: str = _DEFAULT_XML_ENCODING) -> str:
        """
        根据传入的字典创建XML字符串:
            encoding 参数传入 False 时无 <xml version="1.0" ?>
        """

        # 创建 tree.Tree 对象
        root = Tree.fromdict(data)
        itree = Tree(root)

        # 创建 XMLTree 对象
        xmltree = itree.toxml()
        xmlstr = et.tostring(xmltree, encoding=encoding, method="xml")

        return xmlstr.decode()

    @staticmethod
    def _encode_files(boundry: str, files: Dict[str, str]) -> bytes:
        """
        对传入的文件进行编码:
            按照 RFC1867 对传入的文件列表进行编码
            会首先尝试推测文件的 mimetype
            将信息保存后会按照字节流的方式将文件编码至 Bytes 对象

        *boundry: str: 编码边界
        *files: Dict[str: 文件名, str: 文件绝对路径]
        """
        # 文件名模板
        _BOUNDRY = ("--" + boundry).encode()
        _DISPOSITION = "Content-Disposition: form-data; "
        _FILE_FORMAT = "name='{0}'; filename='{1}'"
        _CONTENT_TYPE = "\nContent-Type: {type}"

        # 生成缓冲区保存编码的文件
        buffer = list()

        for filename, location in files.items():
            # 添加文件的基本信息
            rawname = os.path.basename(location)
            mimetype = file.mimetype(location)
            buffer.append(_DISPOSITION.encode())
            format_ = _FILE_FORMAT.format(rawname, filename)
            buffer.append(format_.encode())
            type_ = _CONTENT_TYPE.format(type=mimetype)
            buffer.append(type_.encode())

            # 添加文件内容
            handler = open(location, "rb")
            buffer.append(b"\r\n" + handler.read())
            buffer.append(_BOUNDRY)
            handler.close()

        # 最后添加的一个 boundry 需要补充两个横线 --
        buffer.append("--".encode())

        return b''.join(buffer)

    @staticmethod
    def _encode_paras_str(data: str) -> bytes:
        """
        对传入的参数列表进行编码:
            按照 RFC2616 标准对传入的参数字典进行编码
            判断传入的 data 判断是字符串/字典:
                当为字符串时直接 encode 添加
                当为字典时使用 urlencode 函数处理 encode 添加
        """
        return data.encode()

    @staticmethod
    def _encode_paras_dict(params: dict) -> bytes:
        """
        对传入的参数列表进行编码:
            按照 RFC2616 标准对传入的参数字典进行编码
            判断传入的 data 判断是字符串/字典:
                当为字符串时直接 encode 添加
                当为字典时使用 urlencode 函数处理 encode 添加
        """
        urlencoded: str = urlparse.urlencode(params)
        return urlencoded.encode()

    @staticmethod
    def encode(payload: Union[dict, str] = None,
               files: Optional[dict] = None) -> Tuple[bytes, dict]:
        """对传入的信息进行符合 RFC HTTP/1.1 通讯格式要求的编码"""

        # 生成数据分割 boundry 并对 Header 头进行修改
        buffer = bytes()
        boundry = uuid.uuid4().hex
        additional_header: dict = dict()

        # 检查数据格式修改 Content 头
        if isinstance(payload, dict):
            buffer += WebTools._encode_paras_dict(payload)
            additional_header = _PARAMS_HEADER()
        if isinstance(payload, str):
            buffer += WebTools._encode_paras_str(payload)
            additional_header = _TEXT_HEADER()

        # 检查是否有文件要发送
        if not files is None:
            buffer += WebTools._encode_files(bool, files)
            additional_header = _FILE_HEADER(boundry)

        # 返回所有数据流和 HTTP 请求头
        return buffer, additional_header

    @staticmethod
    def HTTPopener(headers: dict) -> request.OpenerDirector:
        """构建一个支持 cookie 的 HTTPopener - 基于urllib.request"""

        # 添加 cookie 支持
        cookie_jar = http.cookiejar.CookieJar()
        cookie_support = request.HTTPCookieProcessor(cookie_jar)

        # 构建 opener
        opener = request.build_opener(cookie_support, request.HTTPHandler)
        request.install_opener(opener)
        opener.addheaders = list(headers.items())

        return opener

    @staticmethod
    def HTTPConnector(target: str, key: Optional[str] = None,
                      cert: Optional[str] = None) -> http.client.HTTPConnection:
        """
        一个 http/https 链接器

        *target 若为 https 开头则进行 HTTPS 链接
        *cert 若传入则为需要进行连接的证书
        """
        # 获取连接的 host 主机名
        address: tuple = urlparse.urlparse(target)
        host: str = address.netloc

        # 分情况建立连接
        if target.startswith("https://"):
            connection = http.client.HTTPSConnection(
                host, key_file=key, cert_file=cert)
        else:
            connection = http.client.HTTPConnection(host)

        return connection

    @staticmethod
    def _url_combiner(path: str, params: Optional[dict] = None) -> str:
        """url 连接器 - 将传入的 host 和参数合成为 url"""

        # 将连接分解为 host, path, ...
        infomations = urlparse.urlparse(path)
        path = infomations.path

        # 如果 params 为 None 则不进行合并
        if params is None:
            return path

        # 将给定的参数全部合并
        query: str = infomations.query + "&" + urlparse.urlencode(params)

        # 连接 host 和参数
        url: str = urlparse.urljoin(path, '?' + query)
        return url

    @staticmethod
    def _get_charset(response: http.client.HTTPResponse) -> str:
        """尝试从回显 HTTP 头中获得网页编码信息"""

        # Content-Type 格式 "text/html; charset=GB2312"
        content = response.headers.get(_CHARSET)

        # 当 headers-content 中没有提供编码时直接返回默认的 charset
        if content is None:
            return _DEFAULT_CHARSET

        # 当提供了 charset 信息时尝试寻找
        try:
            info = content.split(';')[1]
            info = info.strip(' ')
            charset = info.split('=')[1]
        except IndexError:
            # 获取不到有效编码信息时
            return _DEFAULT_CHARSET
        else:
            return charset

        return _DEFAULT_CHARSET

    @staticmethod
    def _get_compress(response: http.client.HTTPResponse) -> str:
        """尝试获取网页数据的压缩类型"""
        return response.headers.get(_DECOMPRESS, '')

    @staticmethod
    def decompress(rawdata: bytes,
                   response: http.client.HTTPResponse) -> str:
        """尝试解压缩 bytes 类型的 http 数据包"""

        # 获取压缩和编码类型
        compress_method = WebTools._get_compress(response)
        charset = WebTools._get_charset(response)

        # 进行解压
        decompressed = rawdata
        if compress_method == "gzip":
            decompressed = gzip.decompress(rawdata)
        if compress_method == "deflate":
            decompressed = zlib.decompress(rawdata, -zlib.MAX_WBITS)

        # 进行解编码
        return decompressed.decode(charset, "ignore")

    @staticmethod
    def get(target: str, params: Optional[dict] = None,
            cert: Optional[Tuple[str, str]] = None,
            header: Optional[dict] = None)\
            -> Tuple[str, http.client.HTTPResponse]:
        """
        以 Get 方式请求一个 HTTP 目标

        *params 为链接中需要携带的参数
        *cert 为当进行 https 链接时需要的证书:
            首先是 key 文件, 之后是 cert 文件
        *header 为需要指定的 UA
        """

        # 判断是否没有传入 header
        if header is None:
            header = dict()

        # 拼接链接 - 获取 url
        url = WebTools._url_combiner(target, params)
        if cert:
            connection = WebTools.HTTPConnector(target, *cert)
        else:
            connection = WebTools.HTTPConnector(target)
        connection.request("GET", url, headers=header)

        # 获取响应
        response = connection.getresponse()
        rawdata = response.read()
        data = WebTools.decompress(rawdata, response)
        response.close()

        return WebResult(data=data, response=response)

    @staticmethod
    def post(target: str, params: Optional[dict],
             forms: Union[dict, str] = None,
             files: Optional[dict] = None,
             cert: Optional[Tuple[str, str]] = None,
             header: Optional[dict] = None) \
            -> Tuple[str, http.client.HTTPResponse]:
        """
        以 POST 方式请求一个 HTTP 目标

        *params 为链接中需要携带的参数
        *forms 为需要携带的 form 参数/字符串参数
        *files 为需要携带的文件参数
        *cert 为当进行 https 链接时需要的证书:
            首先是 key 文件, 之后是 cert 文件
        *header 为需要指定的 UA
        """

        # 判断是否没有传入 header
        if header is None:
            header = dict()

        # 获取请求需要的 url, payload, 额外 header
        url = WebTools._url_combiner(target, params)
        payload, optional = WebTools.encode(forms, files)
        if cert:
            connection = WebTools.HTTPConnector(target, *cert)
        else:
            connection = WebTools.HTTPConnector(target)

        # 进行请求
        header.update(optional)
        connection.request("POST", url, payload, header)

        # 获取响应
        response = connection.getresponse()
        rawdata = response.read()
        data = WebTools.decompress(rawdata, response)
        response.close()

        return WebResult(data=data, response=response)
