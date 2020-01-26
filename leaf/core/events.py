"""Leaf 事件机制实现"""

from collections import namedtuple
from typing import Optional, List, Callable, NoReturn

from .error import Error
from .wrapper import thread
from .algorithm import Node, Tree


class ReachedMaxReg(Error):
    """达到最大注册数量限制"""
    code = 10011
    description = "项目达到最大注册数量限制"


class InvalidRootName(Error):
    """非法根节点名称"""
    code = 10012
    description = "非法根节点名称"


class InvalidEventName(Error):
    """非法事件名称"""
    code = 10013
    description = "非法事件名称"


class EventNotFound(Error):
    """未找到对应的事件"""
    code = 10014
    description = "未找到对应的事件"


# 对事件需要被调用的参数进行描述
# args - 按照位置的参数: (int, str, ...)
# kwargs - 按照名称的参数: {"sth1": int, "sth2": str, ...}
Parameters = namedtuple("Parameters", ("args", "kwargs"))


class Event:
    """
    事件类:
        name - 事件名
        hook - 注册回调函数到当前事件
        unhook - 取消注册回调函数从当前事件
    """

    def __repr__(self) -> str:
        """返回 repr 信息"""
        return "<Leaf EventObject '" + self.name + "'>"

    def __init__(self, name: str, paras: Parameters,
                 description: Optional[str] = '',
                 maximum: Optional[int] = 0):
        """
        事件类初始化函数:
            parameters - 事件被调用时的参数说明
            name - 该事件的类型: 请遵循 Leaf 中事件名称规定
            description - 事件说明
            maximum - 最大允许注册的回调函数数量: 默认为 0 - 无限
        """
        self.__name: str = name
        self.__maximum: int = maximum
        self.__parameters: Parameters = paras
        self.__description: str = description
        self.__callbacks: List[Callable] = list()

    def __str__(self):
        """str 返回事件的说明"""
        return self.__description

    @property
    def name(self) -> str:
        """返回事件名称"""
        return self.__name

    @property
    def description(self) -> str:
        """返回事件说明"""
        return self.__description

    def hook(self, function: Callable) -> NoReturn:
        """
        注册一个函数到当前的事件:
            function: 在事件被触发时可以被调用的任意函数
        """
        if (self.__maximum == 0) or (len(self.__callbacks) < self.__maximum):
            self.__callbacks.append(function)
        else:
            raise ReachedMaxReg("Reached max registery of event: " + str(self.__maximum))

    def unhook(self, function: Callable) -> NoReturn:
        """
        从注册事件中删除一个函数:
            function: 待删除的函数
        *注意: 当未找到对应函数时不会触发错误
        """
        if function in self.__callbacks:
            self.__callbacks.remove(function)

    @thread
    def notify(self, *args, **kwargs):
        """
        向所有绑定了当前事件的函数发送通知:
            传入的所有参数会原封不动的传入被调用函数
            请确认被调用函数支持参数形式
        *注意: 函数的返回值将会被丢弃
        """
        for function in self.__callbacks:
            try:
                function(*args, **kwargs)
            # pylint: disable=broad-except
            except Exception as _error:
                continue


class Manager:
    """
    事件管理 - 根据传入事件名建立事件区域树
    请遵循 leaf 事件名规则:
        所有的事件需要以 leaf 作为开头
        而后的标识符说明自己的功能区域, 如 plugins
        之后说明自己的业务名称, 如 access_token
        后面添加自定义的事件名, 如 updated
        得到的事件名: leaf.plugins.access_token.updated

        add - 向管理器中添加一个事件
        event - 尝试从指定路径获取一个事件
        names - 尝试从指定路径获取子集下的所有事件名称与说明
    """

    def __repr__(self) -> str:
        """返回 repr 信息"""
        return "<Leaf EventManager '%s'>" % self.__rootname

    def __init__(self, rootname: Optional[str] = "leaf"):
        """初始化事件管理器"""
        self.__rootname: str = rootname
        self.__rootnode: Node = Node(rootname)
        self.__events_tree: Tree = Tree(self.__rootnode)

    def __split(self, name: str, splitor: str) -> list:
        """根据指定的分隔符进行分割"""

        # 当要获取根节点时
        if name == self.__rootname:
            return list()

        # 检查分隔符是否合法
        if not splitor in name:
            raise InvalidEventName("需要以 " + splitor + " 分割")

        joint: list = name.split(splitor)

        # 检查根节点是否合法
        if joint.pop(0) != self.__rootname:
            raise InvalidRootName("Event root must be " + self.__rootname)

        return joint

    def add(self, event: Event) -> NoReturn:
        """
        向事件管理器中添加事件
            event: Event 类型
        """
        # 分割事件名及获取根节点
        current = self.__rootnode
        joint = self.__split(event.name, '.')

        # 迭代搜索每一个子节点
        for tag in joint:
            try:
                current = current.find(tag)
            except KeyError as _error:
                child = Node(tag)
                current.add(child)
                current = child

        # 设置事件作为节点的 value
        current.value = event

    def event(self, name: str) -> Event:
        """
        根据事件名查找对应的事件/事件列:
            当给定的名称对应了一个事件时 - 返回该事件
            当找不到对应节点时 - 报错
        """
        # 分割事件名及获取根节点
        joint = self.__split(name, '.')
        current = self.__rootnode

        # 迭代搜索每一个子节点
        for tag in joint:
            try:
                current = current.find(tag)
            except KeyError as _error:
                raise EventNotFound("事件 " + name + " 不存在")

        # 检查并返回当前节点的事件
        if not isinstance(current.value, Event):
            raise EventNotFound("事件 " + name + " 不存在")

        return current.value

    def names(self, name: str) -> dict:
        """
        返回对应路径下一级中所有的事件名称与说明:
            name("leaf.plugins.access_token") ->
            {
                "updated": "accesstoken更新之后被调用",
                "failed": "accesstoken更新失败之后调用",
                "expired": "accesstoken过期之后调用",
                ...
            }
        """
        # 分割事件名获取根节点
        joint = self.__split(name, '.')
        current = self.__rootnode

        # 迭代搜索节点
        for tag in joint:
            try:
                current = current.find(tag)
            except KeyError as _error:
                raise EventNotFound("事件 " + name + " 不存在")

        # 返回当前节点下所有节点的信息
        result: dict = dict()
        children = current.children()
        for child in children:
            result[child.tag] = str(child.value)

        return result
