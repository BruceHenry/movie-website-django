class LRU:
    max_size = 0
    cache_dict = {}
    head = None
    tail = None

    class Node:
        pre = None
        next = None
        key = None
        value = None

        def __init__(self, key, value):
            self.key = key
            self.value = value

        def __str__(self):
            return str(self.key) + ':' + str(self.value)

        def set(self, value):
            self.value = value

    def __init__(self, max_size=1000):
        self.max_size = max_size

    def get(self, key):
        if key not in self.cache_dict:
            return None
        node = self.cache_dict[key]
        if node != self.head:
            self.__delete_node(node)
            self.__add_to_head(node)
        return node.value

    def set(self, key, value):
        if key not in self.cache_dict:
            node = self.Node(key, value)
            self.cache_dict[key] = node
            self.__add_to_head(node)
        else:
            node = self.cache_dict[key]
            node.set(value)
            if node != self.head:
                self.__delete_node(node)
                self.__add_to_head(node)

    def __add_to_head(self, node):
        node.next = self.head
        node.pre = None
        if self.head is not None:
            self.head.pre = node
        self.head = node
        if self.tail is None:
            self.tail = node
        if len(self.cache_dict) > self.max_size:
            self.cache_dict.pop(self.tail, None)
            self.__delete_node(self.tail)

    def __delete_node(self, node):
        if len(self.cache_dict) == 1:
            self.head = None
            self.tail = None
        elif node == self.head:
            self.head = node.next
            self.head.pre = None
        elif node == self.tail:
            self.tail = node.pre
            self.tail.next = None
        else:
            node.pre.next = node.next
            node.next.pre = node.pre

    def __str__(self):
        result = 'Head | '
        node = self.head
        while node is not None:
            result += str(node) + ' | '
            node = node.next
        result += 'Tail'
        return result
