"""实现一套完整的树算法"""

import queue
from copy import deepcopy
import xml.etree.ElementTree as etree
from typing import \
    Iterable, Iterator, List, Optional, \
    Tuple, NoReturn, Callable, Union


class Node:
    """
    树节点类
    __degree: 保存当前节点的度
    __children: 保存当前节点的子节点列表

    节点类保存当前节点的基础信息
    并且通过一个 list 保存所有子节点的引用
    """

    def __init__(self, tag: Optional[str] = None,
                 value: Optional[object] = None):
        self.__degree = 0
        self.__tag = tag
        self.__value = value
        self.__children = list()

    @property
    def tag(self) -> str:
        """返回当前节点的 Tag"""
        return self.__tag

    @tag.setter
    def tag(self, tag: str):
        """设置当前节点的 tag"""
        self.__tag = tag

    @property
    def value(self) -> object:
        """返回节点的值"""
        return self.__value

    @value.setter
    def value(self, value: object):
        """设置节点的值"""
        self.__value = value

    def __len__(self) -> int:
        """节点的 len 方法返回当前节点的度"""
        return self.__degree

    def __contains__(self, child) -> bool:
        """返回子节点是否在当前节点下"""
        return child in self.__children

    def __getitem__(self, index: int):
        """节点的 getitem 方法返回指定索引位置的子节点引用"""
        if index >= self.__degree:
            raise IndexError('child index out of range')
        return self.__children[index]

    def __iter__(self) -> Iterator:
        """节点的 iter 方法返回子节点的迭代器"""
        return self.children()

    def __hash__(self) -> str:
        """节点的 hash 方法返回标签与值数组的哈希值"""
        return hash((self.__tag, self.__value))

    def __eq__(self, node) -> bool:
        """
        判断两节点是否相同:
            当两个节点的 Tag 与 Value 值均相同时
            判定两节点相同
        """
        return \
            self.value == node.value and \
            self.tag == node.tag

    def __copy__(self):
        """
        节点的浅拷贝方法:
            仅新建一个同名+同值节点
            对于节点的子节点不进行拷贝
        """
        copied = Node(self.tag, self.value)
        copied.adds(self.__children)
        return copied

    def __deepcopy__(self, meno: dict = None, _nil: list = None):
        """
        节点的深拷贝方法:
            构造一个同名+同值节点
            并且递归的将该节点的所有子节点全部复制一份

        *注意: 在深树的根节点调用该方法会造成较大的开销
        """
        copied = Node(
            deepcopy(self.__tag),
            deepcopy(self.__value)
        )

        # 复制每个节点
        for child in self.__children:
            copied.add(deepcopy(child))

        return copied

    def degree(self) -> int:
        """返回当前节点的度 - 等同 len 方法"""
        return self.__degree

    def child(self):
        """按照先进后出的顺序返回当前节点的第一个子节点"""
        return self.__children[self.__degree - 1]

    def remove(self, child) -> NoReturn:
        """
        删除指定的子节点

        *注意: 若指定的子节点在当前节点中未找到
               则不会执行任何操作
        """
        if child in self.__children:
            self.__children.remove(child)
            self.__degree -= 1

    def add(self, child) -> NoReturn:
        """添加一个子节点"""
        self.__degree += 1
        self.__children.append(child)

    def adds(self, nodes: list) -> int:
        """
        向当前节点中添加多个子节点
        返回本次添加节点的个数
        """
        self.__degree += len(nodes)
        self.__children.extend(nodes)

        return len(nodes)

    def find(self, tag: str):
        """根据标签寻找节点"""
        for child in self.children():
            if child.tag == tag:
                return child

        raise KeyError("子节点" + str(tag) + "未找到")

    def children(self, index: int = 0) -> Iterator:
        """返回子节点迭代器 - 等同 iter 方法"""
        while index < self.__degree:
            yield self.__children[index]
            index += 1


class Tree:
    """实现了 DFS+BFS 遍历算法的树类"""

    def __init__(self, root: Node):
        self.__root = root

    def __copy__(self):
        """
        对树进行浅拷贝
        仅仅复制一份当前树的引用
        不拷贝任何值
        """
        return Tree(self.__root)

    def __deepcopy__(self, meno: dict = None, _nil: list = None):
        """
        对整棵树进行深拷贝
        该树中的所有节点及其数据都将被复制
        返回一颗构造的新树

        *注意: 该方法对深树开销较大
        """
        # 调用节点的递归深拷贝
        newroot = deepcopy(self.__root)
        return Tree(newroot)

    @staticmethod
    def _copy(
            from_: Node, to_: Node,
            new_: Callable[[], Node],
            degree_: Callable[[Node], int],
            copy_: Callable[[Node, Node], NoReturn],
            add_: Callable[[Node, Node], NoReturn]
    ) -> NoReturn:
        """
        拷贝树函数
        用户可以自定义传入的更改函数控制拷贝情况

        from_, to_, 两个树的根节点
        new - 新建节点的函数(对第二棵树)
        degree - 获取节点度的函数(对于第一棵树)
        copy - 拷贝值函数(参数为两棵树)
        add - 添加子节点函数(对于第二棵树)
        """
        # 使用 BFS 方式拷贝树
        uncopied = queue.Queue()
        uncopied.put((from_, to_))

        while uncopied.qsize():
            source, destination = uncopied.get()
            # 获取节点的度并赋值给新节点
            degree = degree_(source)
            copy_(source, destination)
            nodes = (new_() for index in range(degree))

            # 向新树上添加节点
            add_(destination, nodes)

            # 添加新的任务
            for index in range(degree):
                uncopied.put((source[index], destination[index]))

    def height(self) -> int:
        """
        计算当前树的高度:
            遍历所有的叶子节点路径
            返回最长的一条长度
        """
        height = 0
        # 遍历叶子节点路径
        for _leaf, path in self.leaves():
            if len(path) > height:
                height = len(path)

        # 添加根节点
        return height + 1

    def biteration(self) -> Iterable[Node]:
        """
        遍历树的节点(不保存节点路径) - BFS
        返回一个节点迭代器, next则步进到下一个节点
        """
        # BFS 遍历法使用队列 - 先进先出保存任务节点
        unvisited = queue.Queue()
        unvisited.put(self.__root)

        # 遍历任务节点
        while unvisited.qsize():
            current = unvisited.get()
            yield current
            if current.degree() == 0:
                continue
            for child in current.children():
                unvisited.put(child)

    def iteration(self) -> Iterable[Node]:
        """遍历树的节点(不保存节点路径) - DFS
        返回一个节点迭代器, next则步进到下一个节点
        """
        # DFS 则使用列表 - 先进后出保存任务节点
        current = self.__root
        unvisited = list()

        # 便利任务节点
        while True:
            yield current
            if current.degree() == 0:
                if not unvisited:
                    return
                current = unvisited.pop()
                continue
            children = list(current.children())
            current = children.pop()
            unvisited.extend(children)

    def parse(self) -> Iterable[Tuple[Node, Tuple[Node, ...]]]:
        """
        遍历树的节点(保存节点路径)
        返回一个节点与路径迭代器:
            从根结点出发, 对子节点进行不断地延拓
            当最后寻找到叶子节点时则可以寻找出一条完整的路径
        """
        # path 列表中存储当前节点和子节点迭代器的元组
        path = list()
        current = self.__root
        iteration = current.children()
        path.append((current, iteration))

        # 向叶子节点迭代
        while True:
            try:
                child = iteration.send(None)
            except StopIteration:
                # 当寻找到叶子节点
                if not path:
                    break
                current, iteration = path.pop()
                continue
            else:
                # 否则迭代出部分路径
                current = child
                purepath = tuple((f for f, s in path))
                yield current, purepath
                path.append((child, iteration))
                iteration = current.children()

    def search(self, target: Node) -> Tuple[Node, ...]:
        """
        搜索树中一个节点的路径:
            如果找到节点则返回路径, 否则返回 None
        """
        # 对 parse 函数给出的所有路径进行查询
        iteration = self.parse()
        for node, path in iteration:
            if node != target:
                continue
            return path

    def leaves(self) -> List[Tuple[Node, Tuple[Node, ...]]]:
        """
        将树的所有叶子节点及其路径输出:
            对 parse 函数给出的所有路径进行判断
            若当前节点为零度节点 - 判定为叶子
        """
        iteration = self.parse()
        result = list()

        # 遍历生成器
        for node, path in iteration:
            if not node.degree() == 0:
                continue
            result.append((node, path))
        return result

    def exist(self, target: Node) -> bool:
        """
        查找树中是否存在指定节点:
            直接使用 BFS 遍历全部节点
            若相同则返回 true

        *该查找仅用于判定, 不能返回对应节点路径
        """
        iteration = self.biteration()
        for node in iteration:
            if node == target:
                return True
        return False

    def toxml(self, attribute: Optional[str] = None,
              text: Optional[str] = None) -> etree.Element:
        """导出至xml.etree.cElementTree.Element

        *attribute, text 指定 value 中对应
        Node节点value 中属性与text值
        """
        # 检查 attr & text 键
        attribute = '' if attribute is None else attribute
        text = '' if text is None else text

        # 新建树根节点并设定当前树节点
        et = etree.Element(None)
        root = self.__root

        # 构造新建节点的函数
        def new() -> etree.Element:
            return etree.Element(None)

        # 获取节点的度
        def degree(node: Node) -> int:
            return node.degree()

        # 赋值节点函数
        def copy(treenode: Node, etnode: etree.Element) -> NoReturn:
            etnode.tag = treenode.tag

            # 如果 value 值为字典则按照键拷贝
            if isinstance(treenode.value, dict):
                etnode.attrib = treenode.value.get(attribute)
                etnode.text = treenode.value.get(text)

            # 如果是单纯的一个值
            else:
                # 如果 value 为 None 则设置为空
                if treenode.value is None:
                    etnode.text = ''
                else:
                    etnode.text = str(treenode.value)

        # 添加至新节点函数
        def add(target: etree.Element,
                nodes: Iterable[etree.Element]):
            return target.extend(nodes)

        Tree._copy(root, et, new, degree, copy, add)
        return et

    @staticmethod
    def fromxml(et: etree.Element,
                text: Union[bool, str],
                attribute: Union[bool, str]
                ) -> Node:
        """
        从xml.etree.cElementTree.Element中导入

        *attribute, text 指定 value 中对应 etree节点的属性与 text 值
        当不传入 attribute 时 - value 对应的值为 text
        当不传入 text 时 - value 对应的值为 attribute
        当都传入时 - value 为对应键组成的 dict
        当都不传入时 - value 为空字符串
        """
        # 目标赋值节点
        root = Node(None)

        # 新建节点的函数
        def new() -> Node:
            return Node(None)

        # 获取节点的度
        def degree(node: Node) -> int:
            return len(node)

        # 赋值节点函数
        def copy(etnode: etree.Element, treenode: Node) -> NoReturn:
            treenode.tag = etnode.tag

            # 判断需要记录的信息
            if text and not attribute:
                treenode.value = etnode.text
            if attribute and not text:
                treenode.value = etnode.attrib
            if attribute and text:
                treenode.value = dict()
                treenode.value[attribute] = etnode.attrib
                treenode.value[text] = etnode.text

        # 添加至新节点函数
        def add(target: Node, nodes: Iterable[Node]) -> int:
            return target.adds(list(nodes))

        Tree._copy(et, root, new, degree, copy, add)
        return root

    @staticmethod
    def fromdict(treedict: dict) -> Node:
        """
        fromdict 从字典中导入数据
        只允许有一个根节点, 如果根节点发现多个字典则报错
        字典的 key 用作树的tag, 如果是 字符串 k-v 模式
        则认为为叶子节点, value 存储为 v 的字符串,
        当发现 list 时将 k 扩展开赋值节点,
        当发现 tuple 时将 tuple 整体保存至 value

        将此方法抽象至 _copy 较为困难, 所以单独写出
        """
        treenode = root = Node(None)
        uncopied = queue.Queue()
        dictnode = tuple(treedict.items())[0]
        uncopied.put((dictnode, root))

        # 检查根节点数量是否为1
        if not len(treedict) == 1:
            raise ValueError('Should be only one root node')
        if isinstance(dictnode[1], list):
            raise ValueError('Should be only one root node')

        while uncopied.qsize():
            dictnode, treenode = uncopied.get()
            key, value = dictnode

            # 当获取到的 value 不是 dict 为叶子节点
            if not isinstance(value, dict):
                treenode.tag = key
                treenode.value = value
                continue

            # 对当前节点命名, 并探测所有子节点
            treenode.tag = key
            items = tuple(value.items())

            for key, childvalue in items:

                # 如果下一层中某节点 A 为列表, 则要将 A 节点
                # 的所有子元素提升至当前层
                if isinstance(childvalue, list):
                    for item in childvalue:
                        newnode = Node(None)
                        treenode.add(newnode)
                        uncopied.put(((key, item), newnode))
                    continue

                # 否则当下一层是字典元素时按正常添加
                newnode = Node(None)
                treenode.add(newnode)
                uncopied.put(((key, childvalue), newnode))

        return root

    def todict(self, index: Optional[int] = None,
               _dict: Optional[dict] = None) -> dict:
        """导出至字典"""
        # 创建未拷贝任务队列并指定根节点为第一个任务节点
        treedict = _dict if _dict else dict()
        uncopied = queue.Queue()
        uncopied.put((self.__root, treedict))

        # 遍历任务队列
        while uncopied.qsize():
            treenode, dictnode = uncopied.get()

            # 当该节点名已经存在时 - 将子内容提升为列表
            if treenode.tag in dictnode.keys():
                previous_data = dictnode[treenode.tag]
                dictnode[treenode.tag] = list()
                dictnode[treenode.tag].append(previous_data)

                # 判断是否为叶子节点
                if treenode.degree() == 0:
                    if index is None:
                        text = treenode.value
                    else:
                        text = treenode.value[index]
                    dictnode[treenode.tag].append(text)
                    continue

                next_level = dict()
                dictnode[treenode.tag].append(next_level)
                dictnode = next_level

            # 否则创建新键添加内容
            else:

                # 判断是否为叶子节点
                if treenode.degree() == 0:

                    # 检查是否需要取键
                    if index is None:
                        dictnode[treenode.tag] = treenode.value
                    else:
                        dictnode[treenode.tag] = treenode.value[index]
                    continue

                dictnode[treenode.tag] = dict()
                dictnode = dictnode[treenode.tag]

            for child in treenode:
                uncopied.put((child, dictnode))

        return treedict
