"""
错误代码管理器:
    管理现有的错误代码与描述
    为新的请求计算颁发错误代码
    生成错误代码描述文档
"""

# 将文件路径向上转移
import argparse as _argparse
from collections import namedtuple as _namedtuple
from typing import List as _List
from typing import Dict as _Dict

# pylint: disable=wrong-import-position
__import__("os").chdir("..")
from leaf.core import error as _error

# 设定错误信息存储类
ErrorInfo = _namedtuple("ErrorInfo", ("description", "module"))

# 获取 error.Error 的所有子类信息
__informations: _Dict[int, str] = dict()


def reload():
    """利用反射导出所有的错误信息"""
    __subclasses: _List[_error.Error] = _error.Error.__subclasses__()
    for _error_class in __subclasses:
        info = ErrorInfo(_error_class.description, _error_class.__module__)
        __informations[_error_class.code] = info


# markdown 表头
__HEADER = \
    """
以下是 _Leaf_ 的现有的所有错误代码及其描述:

| 错误代码 | 错误描述 | 所属模块 |
| :----: | | :----: | :----: |
"""


# 命令行参数接收
__parser = _argparse.ArgumentParser()
__parser.add_argument("--export", "-e", default="errcode.md",
                      help="export 参数表示导出的文件名, 默认为: errcode.md")


def __makeline(key: int, info: ErrorInfo) -> str:
    """制作新的一行"""
    return "| " + str(key) + " | " + \
        info.description + " | " + info.module + " |"


def export(filename: str) -> _Dict[int, ErrorInfo]:
    """导出文件"""

    # 切换到当前目录
    __import__("os").chdir("docs")

    content_list = list()
    for key, value in __informations.items():
        content_list.append(__makeline(key, value))

    with open(filename, 'w') as handler:
        content = __HEADER + '\n'.join(content_list)
        handler.write(content)

    print("Exported errcodes to file '" + filename + "'.")
    __import__("os").chdir("..")
    return __informations


reload()
if __name__ == "__main__":
    args = __parser.parse_args()
    export(args.export)
