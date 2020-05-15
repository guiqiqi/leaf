"""实现一个支持上下文管理器的有限状态机"""

import string
from typing import List, Set, Dict, Tuple, NoReturn, Optional, Any

from ..error import Error
from ..tools.time import TimeTools as timetools
from ..tools.encrypt import EncryptTools as enctools


class StateExistError(Error):
    """状态码已经存在错误"""
    code = 11001
    description = "该状态码已经被使用, 请更换状态码"


class EventNotAccept(Error):
    """事件不在当前状态的接受范围内"""
    code = 11002
    description = "当前状态不接受发生的指定事件"


class DestinationNotExist(Error):
    """当前状态与事件不能确定转移的目标状态"""
    code = 11003
    description = "根据当前状态和事件不能确定转移的目标状态"


class Event:
    """事件类"""
    description: str = str()

    def action(self, *args, **kwargs) -> Any:
        """接口函数 - 用于指示事件动作"""

    def __repr__(self) -> str:
        """返回 repr 信息"""
        return "<Leaf FSM-Event>"

    def __hash__(self) -> int:
        """返回当前事件的哈希值 - 函数的hash"""
        return hash(self.__opcode)

    def __init__(self):
        """
        事件类构造函数:
            opcode: 当前时间的事件码 - 随机
            time: 事件发生的事件
            result: 在动作发生之后用于保存动作函数的相关值
        """
        self.__time: int = timetools.now()
        self.__opcode: str = enctools.random(
            16, string.digits + string.ascii_letters)
        self.__extra: dict = dict()

    def append(self, key, value) -> NoReturn:
        """给当前的事件添加额外信息描述"""
        self.__extra[key] = value

    @property
    def extra(self) -> dict:
        """返回事件的额外信息"""
        return self.__extra

    @property
    def time(self) -> int:
        """返回事件发生时间"""
        return self.__time

    @property
    def opcode(self) -> str:
        """返回事件的操作码"""
        return self.__opcode


class State:
    """状态类"""
    # 静态变量 - 保存已经生成的状态码
    __codes: Set[int] = set()

    def __repr__(self) -> str:
        """返回 repr 信息"""
        return "<Leaf FSM-State code " + str(self.__code) + ">"

    def __hash__(self) -> int:
        """使得状态可哈希 - 返回当前状态 hash(code)"""
        return hash(self.__code)

    def __init__(self, code: int, description: str):
        """
        状态类构造函数:
            code: 状态对应状态码 - 整型变量
            description: 当前状态的描述
            extra: 当前状态的额外描述信息
        """
        self.__code = code
        self.__description = description
        self.__extra = dict()
        if self.__code in self.__codes:
            raise StateExistError("状态码已经存在 - " + int(code))

        self.__codes.add(code)
        self.__accepted_events: List[Event] = list()

    def add(self, event: Event) -> NoReturn:
        """添加当前状态接受的动作"""
        self.__accepted_events.append(event)

    @property
    def code(self) -> int:
        """返回状态码"""
        return self.__code

    @property
    def description(self) -> str:
        """返回状态说明"""
        return self.__description

    @property
    def extra(self) -> dict:
        """返回当前状态的额外信息"""
        return self.__extra

    @extra.setter
    def extra_setter(self, extra: dict) -> NoReturn:
        """设置当前状态的额外信息"""
        self.__extra = extra

    def accept(self, event: Event) -> bool:
        """检查当前的状态是否接受指定的事件"""
        event_class = getattr(event, "__class__", None)
        if event_class in self.__accepted_events:
            return True
        return False

    def enter(self, reason: Optional[Event] = None) -> NoReturn:
        """
        进入状态时执行的函数 - 接口
        传入由什么事件导致进入该状态
        """

    def exit(self, reason: Optional[Event] = None) -> NoReturn:
        """
        退出当前状态时执行的函数 - 接口
        传入因为什么事件导致退出该状态
        """


class Machine:
    """状态管理器"""

    def __repr__(self) -> str:
        """返回 repr 信息"""
        return "<Leaf FSM-Machine '" + self.__name + "'>"

    def __init__(self, name: str):
        """
        状态管理器:
            name: 当前状态机的名称
            current: 当前状态
            recorder: 事件记录器
            transitions: 变化状态表
                {
                    (OriginState, Action): DestState,
                    ...
                }
        """
        self.__name: str = name
        self.__current: State = None
        self.__recorder: List[Event] = list()
        self.__transitions: Dict[Tuple[State, Event], State] = dict()

    @property
    def current(self) -> State:
        """返回当前状态"""
        return self.__current

    @property
    def name(self) -> str:
        """返回状态机名称"""
        return self.__name

    @property
    def events(self) -> List[Event]:
        """返回所有发生过的事件"""
        return self.__recorder

    def handle(self, event: Event, *args, **kwargs) -> NoReturn:
        """
        对当前状态改变转移, 当发生了一个指定的事件时, 执行顺序如下:
            0. 判断这个事件是否被当前状态接受
            1. 如果接受, 执行当前状态的 exit 函数
            2. 执行指定事件的 action 函数
            3. 执行转移目标状态的 enter 函数
            4. 记录发生的事件信息

        *args, **kwargs 参数将被传递给当前事件的执行函数
        """
        if not self.__current.accept(event):
            raise EventNotAccept("当前状态不允许事件该事件发生")

        try:
            event_class = getattr(event, "__class__", None)
            destination: State = self.__transitions[(
                self.__current, event_class)]
        except KeyError as _error:
            raise DestinationNotExist("找不到目标状态: " + str(_error.args))

        self.__current.exit(event)
        event.action(*args, **kwargs)
        destination.enter(event)
        self.__current = destination
        self.__recorder.append(event)

    def add(self, origin: State, event: Event, destination: State) -> NoReturn:
        """给状态转移表中添加一条记录"""
        self.__transitions[(origin, event)] = destination

    def start(self, state: State) -> NoReturn:
        """启动状态机运行初始进入函数"""
        self.__current = state
        self.__current.enter()

    def stop(self) -> NoReturn:
        """当确定状态机到达最终状态时可以执行该函数用于退出最终状态"""
        self.__current.exit()
        self.__current = None
