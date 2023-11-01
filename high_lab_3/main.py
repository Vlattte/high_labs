class Node:
    def __init__(self, value):
        self.__value = value
        self.__left_child = None
        self.__right_child = None

    def __str__(self):
        return f"{self.__value}"

    def __iter__(self):
        yield from self._print_subtree()

    def add_node(self, value):
        """ Добавление узла в дерево """

        if value < self.__value:
            if self.__left_child:
                self.__left_child.add_node(value)
            else:
                self.__left_child = Node(value)
        elif value > self.__value:
            if self.__right_child:
                self.__right_child.add_node(value)
            else:
                self.__right_child = Node(value)

    def _print_subtree(self):
        """  """
        if self.__left_child:
            yield from self.__left_child._print_subtree()
        yield self.__value
        if self.__right_child:
            yield from self.__right_child._print_subtree()


n = Node(5)
n.add_node(7)
n.add_node(8)
n.add_node(1)
n.add_node(3)
n.add_node(0)
n.add_node(-2)
for node in n:
    print(node)
