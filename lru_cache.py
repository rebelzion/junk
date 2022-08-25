"""
LRU Cache:
O(1) lookup
O(1) insert
"""

import time

class _LRUCache:
    class _Node:

        def __init__(self, key, value):
            self.key = key
            self.value = value
            self.next = None
            self.prev = None

    def __init__(self, func, size: int = 10, debug=False):
        self.func = func
        self.size = size
        self.cache = {} # key to linked list node
        self.lru_list = None
        self.lru_last = None
        self.debug = debug

    def __call__(self, *args, **kwargs):

        result = None
        # check if args is in the cache
        if args in self.cache:
            # move it to the front of the list
            self._move_node_to_head(self.cache[args])
            result = self.cache[args].value
        else:
            # if it is not, add it to the front of the list and cache it
            if len(self.cache) == self.size:
                # remove the last node from the list
                key, _ = self._remove_last_node()
                del self.cache[key]

            # add the node to the front of the list
            result = self.func(*args, **kwargs)
            node = self._Node(key=args, value=result)
            self.cache[args] = node
            self._add_node_to_head(node)

        print(self)
        return result

    def _move_node_to_head(self, node):
        if node == self.lru_list and node == self.lru_last:
            return
        if node == self.lru_list:
            return
        if node == self.lru_last:
            self.lru_last = node.prev
            self.lru_last.next = None
        else:
            node.prev.next = node.next
            node.next.prev = node.prev
        self._add_node_to_head(node)

    def _remove_last_node(self):
        value = None
        if self.lru_last:
            key = self.lru_last.key
            value = self.lru_last.value
            self.lru_last = self.lru_last.prev
            self.lru_last.next = None
        return key, value

    def _add_node_to_head(self, node):
        node.next = self.lru_list
        if self.lru_list:
            self.lru_list.prev = node
        else:
            self.lru_last = node
        self.lru_list = node


    def __repr__(self) -> str:

        repr = ""

        node = self.lru_list
        while node:
            repr += f"[{node.key} | {node.value}]-->"
            node = node.next
        return repr

def LRUCache(func=None, size=10, debug=False):
    if func:
        return _LRUCache(func, size, debug)
    else:
        def wrapper(func):
            return _LRUCache(func, size, debug)
        return wrapper


@LRUCache(size=3, debug=True)
def f(x):
    print(f"calculating x**2, will take {1} seconds ...")
    time.sleep(1)
    return x**2


if __name__ == "__main__":
    f(2)
    f(2)
    f(2)
    f(3)
    f(4)
    f(3)
    f(2)
    f(5)
