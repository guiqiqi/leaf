"""
错误代码管理器:
    管理现有的错误代码与描述
    生成错误代码描述文档
"""

# 将文件路径向上转移
import os as _os
import json as _json
import argparse as _argparse
from collections import namedtuple as _namedtuple
from collections import OrderedDict as _ODict
from typing import List as _List
from typing import Dict as _Dict

workdir: str = _os.path.dirname(_os.path.realpath(__file__))
__import__("sys").path.append(_os.path.dirname(workdir))

# pylint: disable=wrong-import-position
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
__parser = _argparse.ArgumentParser(description="错误代码导出")
__parser.add_argument("--type", "-t", default="markdown",
                      help="type 表示导出文件类型, 支持 json, markdown. 默认为: markdown")
__parser.add_argument("--export", "-e", help="export 参数表示导出的文件名", required=True)


def __makeline(key: int, info: ErrorInfo) -> str:
    """制作新的一行"""
    return "| " + str(key) + " | " + \
        info.description + " | " + info.module + " |"


def __markdown(informations: _Dict[int, ErrorInfo]) -> str:
    """制作 markdown 格式的表格"""
    content_list = list()
    informations = _ODict(sorted(informations.items()))
    for key, value in informations.items():
        content_list.append(__makeline(key, value))
    return '\n'.join(content_list)


def __json(informations: _Dict[int, ErrorInfo]) -> str:
    """制作 json 格式的数据"""
    errcodes: _Dict[int, _Dict[str, str]] = dict()
    for code, info in informations.items():
        errcodes[code] = dict(info._asdict())

    return _json.dumps(errcodes, indent=4, sort_keys=True, ensure_ascii=False)


def export(filename: str, _type: str) -> _Dict[int, ErrorInfo]:
    """导出文件"""

    content = ''
    if _type == "markdown":
        content = __HEADER + __markdown(__informations)
    if _type == "json":
        content = __json(__informations)

    with open(filename, 'w', encoding="utf-8") as handler:
        handler.write(content)

    # 完成导出, 切换出当前目录
    print("错误代码已导出到文件 '" + filename + "'")

    return __informations


reload()
if __name__ == "__main__":
    args = __parser.parse_args()
    export(args.export, args.type)
