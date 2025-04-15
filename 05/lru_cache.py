class Node:
    def __init__(self, key=-1, val=-1):
        self.val = val
        self.key = key
        self.next = None
        self.prev = None


class DLL:
    def __init__(self):
        self.start = Node()
        self.finish = Node()
        self.start.next = self.finish
        self.finish.prev = self.start

    def append(self, node):
        left, right = self.finish.prev, self.finish
        left.next = node
        node.next = right
        node.prev = left
        right.prev = node

    def delete(self, node):
        left, right = node.prev, node.next
        left.next = right
        right.prev = left
        return node

    def move_to_finish(self, node):
        self.append(self.delete(node))

    def popleft(self):
        return self.delete(self.start.next)


class LRUCache:
    def __init__(self, limit: int = 4):
        self.hm = {}
        self.dll = DLL()
        self.cap = limit
        if self.cap < 0:
            raise ValueError("Limit must be non-negative!")

    def get(self, key):
        if key not in self.hm:
            return None

        node = self.hm[key]
        self.dll.move_to_finish(node)
        return node.val

    def set(self, key, value) -> None:
        if key in self.hm:
            node = self.dll.delete(self.hm[key])
            node.val = value
        else:
            node = Node(key, value)
            self.hm[key] = node
        self.dll.append(node)

        if len(self.hm) > self.cap:
            self.hm.pop(self.dll.popleft().key)


# if __name__ == "__main__":
#     cache = LRUCache(2)

#     cache.set("k1", "val1")
#     cache.set("k2", "val2")

#     assert cache.get("k3") is None
#     assert cache.get("k2") == "val2"
#     assert cache.get("k1") == "val1"

#     cache.set("k3", "val3")

#     assert cache.get("k3") == "val3"
#     assert cache.get("k2") is None
#     assert cache.get("k1") == "val1"
