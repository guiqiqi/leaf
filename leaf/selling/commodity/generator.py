"""使用树算法根据产品生成商品信息"""

from queue import Queue

from typing import List
from typing import NoReturn

from .stock import Stock
from .product import Product
from .product import ProductParameter

from ...core.algorithm import tree


class StocksGenerator:
    """
    使用树算法根据传入的产品信息生成商品并设置
    """

    def __init__(self, product: Product) -> NoReturn:
        """
        类初始化函数:
            product: 要使用进行生成的产品信息
        """
        self.__product = product
        self.__stocks: List[Stock] = list()

    @property
    def goods(self) -> List[Stock]:
        """返回内存中的所有商品列表"""
        return self.__stocks

    def setall(self, price: float, currency: str, inventory: int) -> NoReturn:
        """
        对所有的商品设置统一信息:
            price: 商品价格
            currency: 商品价格货币
            inventory: 商品库存
        """
        for good in self.__stocks:
            good.price = price
            good.currency = currency
            good.inventory = inventory

    @staticmethod
    def _generate(product: Product) -> tree.Tree:
        """
        使用 BFS 算法生成一棵产品信息树:
            0. 生成 None 的根节点, 将根节点加入任务队列
            1. 将当前遍历属性的 index 加入任务节点
            2. 获取任务节点以及需要添加的信息
            3. goto 0 until tasks.qsize() == 0
        """
        index, root, height = 0, tree.Node(None), len(product.parameters)
        tasks = Queue()
        tasks.put((root, index))

        # 开始 BFS 的主循环
        while tasks.qsize():
            node, index = tasks.get()
            option: ProductParameter = product.parameters[index]
            children = [tree.Node(option.name, selection)
                        for selection in option.options]
            node.adds(children)
            if index == height - 1:
                continue
            for task in children:
                tasks.put((task, index + 1))

        return tree.Tree(root)

    @staticmethod
    def _traverse(infotree: tree.Tree) -> List[dict]:
        """遍历所有的叶子节点路径, 将节点信息取出之后update"""
        goods = list()

        for leaf, path in infotree.leaves():
            attributes = dict()
            # 加入叶子结点的信息
            attributes.update({leaf.tag: leaf.value})

            for node in path:
                attributes.update({node.tag: node.value})

            # 将根节点的无意义数据 pop 出去
            attributes.pop(None)
            goods.append(attributes)

        return goods

    def clean(self) -> int:
        """
        对现有的产品信息中的旧商品信息进行清理
        这个操作会清除数据库中所有产品生成的商品记录
        """
        # pylint: disable=no-member
        return Stock.objects(product=self.__product).delete()

    def save(self) -> int:
        """将内存中的所有商品对象入库"""
        rows = len(self.__stocks)
        for good in self.__stocks:
            good.save()

        self.__stocks = []
        return rows

    def calculate(self) -> NoReturn:
        """生成与遍历树 - 内存中生成所有的商品对象"""
        ctree = self._generate(self.__product)
        attributes = self._traverse(ctree)

        for attribute in attributes:
            good = Stock(individual=False,
                         product=self.__product,
                         name=self.__product.name,
                         attributes=attribute,
                         description=self.__product.description,
                         addition=self.__product.addition,
                         tags=self.__product.tags)
            self.__stocks.append(good)
