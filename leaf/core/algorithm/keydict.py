"""实现一个支持通过 . 操作符访问键的字典类"""

from typing import Hashable, NoReturn, Tuple
# from multiprocessing.managers import BaseProxy


class AttrDict(dict):
    """通过重写 __getattr__ 操作符使得字典支持 . 操作符访问"""

    _functions = {
        "keys", "fromkeys", "values", "setdefault", "update", "get",
        "clear", "popitem", "copy", "items", "pop"
    }

    def __setattr__(self, key: Hashable, value: object) -> NoReturn:
        """向字典的值和 attr 同时添加一份"""
        super().__setitem__(key, value)
        # super().__setattr__(key, value)

    def __getattr__(self, key: str) -> object:
        """重定向至 __getitem__"""

        # 当访问实例函数时返回函数对象
        if key in self._functions:
            return super().__getattribute__(key)

        return self[key]

    def __getstate__(self) -> Tuple[dict, dict]:
        """对象的 pickle 序列化封装函数"""
        return self.__dict__, dict(self)

    def __setstate__(self, state: Tuple[dict, dict]) -> NoReturn:
        """对象的序列化恢复"""
        self.__dict__.update(state[0])
        super().update(state[1])


class StaticDict(AttrDict):
    """继承自 AttrDict 但是不允许修改数据"""

    def __setattr__(self, key: Hashable, value: object):
        """删除设置功能"""
        raise RuntimeError("StaticDict cannot be set value")

    def __delattr__(self, key: Hashable):
        """删除删除功能"""
        raise RuntimeError("StaticDict cannot be remove value")
