"""
接入点代码管理器:
    管理现有的接入点
    根据视图函数生成接入点信息
"""

# 将 leaf 加入临时目录并引用
import json
import os as _os
from typing import Optional
from typing import Callable
from typing import NoReturn
from typing import List, Tuple
from functools import namedtuple
from collections import defaultdict
import argparse as _argparse

workdir: str = _os.path.dirname(_os.path.realpath(__file__))
__import__("sys").path.append(_os.path.dirname(workdir))

# pylint: disable=wrong-import-position
import leaf as _leaf

AccessRoute = namedtuple("AccessRoute", ("path", "methods"))
AccessPoint = namedtuple("AccessPoint", ("name", "description"))

Static = _leaf.core.algorithm.StaticDict
CRITICAL, FATAL, ERROR = 50, 50, 40
WARNING, INFO, DEBUG, NOTSET = 30, 20, 10, 0

# 生成临时使用核心模块配置
basic = Static({
    "domain": "accesspoint.manage",
    "locker": ".ap-testconfig-leaf.lock",
    "manager": None,
    "authkey": "password"
})

logging = Static({
    "level": INFO,
    "rcfile": ".hidden.leaf.log",
    "format": None,
    "console": Static({
        "level": DEBUG,
        "format": None
    }),
    "file": Static({
        "level": ERROR,
        "format": None
    })
})

# 生成 leaf 应用实例
init = _leaf.Init()
init.kernel(basic)
init.logging(logging)
application = init.server()

# 获取所有的视图函数与接入点映射
_functions = application.view_functions
_paths = {ap.endpoint: AccessRoute(ap.rule, tuple(ap.methods)) for
          ap in application.url_map.iter_rules()}
urlmap = {_paths[key]: _functions[key] for key in _functions.keys()}
accesspoints = list()

# markdown 表头
__HEADER = \
    """
以下是 _Leaf_ 现有的所有接入点信息及其介绍:

| 接入点代码 | 接入点描述 | 接入点路径 | 允许的请求方式 |
| :------ | | :---- | | :----- | | :----------- |
"""


# 命令行参数接收
__parser = _argparse.ArgumentParser(description="接入点信息导出")
__parser.add_argument("--type", "-t", default="markdown",
                      help="type 表示导出文件类型, 支持 json, markdown. 默认为: markdown")
__parser.add_argument("--export", "-e", help="export 参数表示导出的文件名", required=True)


def __makeline(info: Tuple[str]) -> str:
    """制作新的一行"""
    return "| " + " | ".join(info) + " |"


def __markdown(infos: List[Tuple[str]]) -> str:
    """制作 markdown 格式的数据"""
    lines = list()
    for info in infos:
        lines.append(__makeline(info))
    return __HEADER + '\n'.join(lines)


def __json(infos: List[Tuple[str]]) -> str:
    """制作 JSON 格式的数据"""
    lines = defaultdict(list)
    for info in infos:
        lines[info[0]].append(info[1:4])
    return json.dumps(lines, indent=4, sort_keys=True, ensure_ascii=False)


def unclosure(func: Callable, env: Optional[List[Tuple]] = None) -> \
    Tuple[Callable, List[Tuple]]:
    """
    从闭包函数中迭代的找出最底层包装的函数
    并逐层的统计闭包环境信息以列表返回
    """
    if env is None:
        env = list()

    # 如果是不是包底函数
    if "__closure__" in dir(func) and func.__closure__:

        # 被闭包的下一层函数
        next_stage: Callable = None
        stage_env = list()

        # 提取所有的闭包环境参数
        for envinfo in func.__closure__:
            content = envinfo.cell_contents
            if callable(content):
                next_stage = envinfo.cell_contents
                continue
            stage_env.append(content)

        env.append(tuple(stage_env))
        return unclosure(next_stage, env)

    # 如果是包底函数
    return func, env


def doc(func: Callable) -> str:
    """处理底包函数的注释"""
    docs = func.__doc__.split('\n')
    first = docs[0] if docs[0] else docs[1]
    exhint = first.split('-')[0].strip()
    return exhint


def pointname(env: List[Tuple]) -> str:
    """
    从闭包的信息中匹配访问点名称
    所有的接入点名称以 leaf. 开头
    当未找到对应的接入点名称时返回 None
    """
    for layer in env:
        for info in layer:
            if isinstance(info, str) and info.startswith("leaf."):
                return info
    return None


def reload() -> NoReturn:
    """加载所有的接入点信息"""
    # pylint: disable=global-statement
    global accesspoints

    for route, func in urlmap.items():
        bottom, env = unclosure(func)
        description = doc(bottom)
        name = pointname(env)

        # 跳过无接入点函数
        if name is None:
            continue

        accesspoints.append((
            name, description, route.path,
            ", ".join(route.methods)
        ))

    sorted(accesspoints, key=lambda item: item[0])


def export(filename: str, _type: str) -> NoReturn:
    """导出文件"""

    content = ''
    if _type == "markdown":
        content = __markdown(accesspoints)
    if _type == "json":
        content = __json(accesspoints)

    with open(filename, 'w', encoding="utf-8") as handler:
        handler.write(content)

    # 完成导出, 切换出当前目录
    print("错误代码已导出到文件 '" + filename + "'")


reload()
if __name__ == "__main__":
    args = __parser.parse_args()
    export(args.export, args.type)
