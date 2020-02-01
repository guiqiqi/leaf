"""
用来统计 Leaf 系统中使用了哪一些 Errcode
防止使用冲突, 并且可以计算颁发 Errcode 给模块
"""

import atexit
from ast import literal_eval
from typing import IO, Set, NoReturn, Tuple

from leaf.core import error
from leaf.core.tools import file


# 系统错误码范围
__CODE_RANGE = range(
    error.MIN_LEAF_ERRCODE,
    error.MAX_LEAF_ERRCODE
)

# 配置文件
__CONF_FILE = "errcode.ini"


class Recorder:
    """错误码记录器"""

    def __init__(self, filename: str):
        """
        记录器构造函数:
            filename: 配置文件名
        """
        self.__filename: str = filename
        self.__handler: IO = open(filename, 'r+', encoding="utf-8")
        self.load()

    @property
    def codecs(self) -> set:
        """返回已经使用的codecs"""
        return self.__codes

    @property
    def config(self) -> dict:
        """返回当前配置"""
        return self.__config

    def load(self) -> dict:
        """
        读取当前配置:
            config: 当前的配置
            codes: 已经被占用的codes
        """
        self.__config = file.read_config(self.__handler)
        self.__codes = set()

        for _holder, setting in self.__config.items():
            self.__codes.update(literal_eval(setting["codes"]))

        return self.__config

    def add(self, holder: str, codes: Set[int], description: str) -> NoReturn:
        """
        增加一条错误代码记录:
            holder: 错误代码被颁发给谁了
            codes: 所需要占用的错误代码Set
            description: 描述
        """
        # 当已经有记录需要添加一部分错误码时
        if holder in self.__config.keys():
            _codestr = self.__config[holder]["codes"]
            held: Set[int] = literal_eval(_codestr)
            held = str(held.union(codes))
            file.edit_config(self.__handler, (holder, "codes", held))
            self.load()
            return

        # 当不存在时新建记录
        file.write_config(self.__handler, {
            holder: {
                "codes": str(codes),
                "description": description
            }
        })
        self.load()

    def check(self, code: int) -> bool:
        """检查code是否被占用"""
        return code in self.__codes

    def issue(self, count: int) -> Tuple[int, int]:
        """
        颁发一个错误代码段给程序:
            count: 需要的错误代码数量
        """
        # 如果是空直接返回
        if not self.__codes:
            return (error.MIN_LEAF_ERRCODE,
                    error.MIN_LEAF_ERRCODE + count)

        codes = sorted(self.__codes)
        for index in range(len(codes) - 1):
            if (codes[index + 1] - codes[index]) > count:
                return (codes[index], codes[index + 1])

        # 检查最后一个区段
        if codes[-1] - codes[-2] > count:
            return (codes[-2], codes[-1])

        # 无可用
        return (0, 0)

    def save(self) -> NoReturn:
        """保存设置文件"""
        self.close()
        self.__handler = open(self.__filename, 'r+', encoding="utf-8")

    def close(self) -> NoReturn:
        """关闭设置文件句柄"""
        self.__handler.close()


recorder = Recorder(__CONF_FILE)
atexit.register(recorder.close)
