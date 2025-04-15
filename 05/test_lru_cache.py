import pytest

from lru_cache import (
    LRUCache,
    Node,
    DLL,
)


class TestNode:
    def test_node_creation(self):
        node = Node(key=1, val="test")
        assert node.key == 1
        assert node.val == "test"
        assert node.next is None
        assert node.prev is None


class TestDLL:
    @pytest.fixture
    def dll(self):
        return DLL()

    def test_initialization(self, dll):
        assert isinstance(dll.start, Node)
        assert isinstance(dll.finish, Node)
        assert dll.start.next == dll.finish
        assert dll.finish.prev == dll.start

    def test_append(self, dll):
        node = Node(1, "a")
        dll.append(node)
        assert dll.start.next == node
        assert dll.finish.prev == node

    def test_delete(self, dll):
        node = Node(1, "a")
        dll.append(node)
        deleted = dll.delete(node)
        assert deleted == node
        assert dll.start.next == dll.finish
        assert dll.finish.prev == dll.start

    def test_move_to_finish(self, dll):
        node1 = Node(1, "a")
        node2 = Node(2, "b")
        dll.append(node1)
        dll.append(node2)
        dll.move_to_finish(node1)
        assert dll.finish.prev == node1
        assert node1.prev == node2

    def test_popleft(self, dll):
        node = Node(1, "a")
        dll.append(node)
        popped = dll.popleft()
        assert popped == node
        assert dll.start.next == dll.finish


class TestLRUCache():
    @pytest.fixture
    def cache(self):
        return LRUCache(2)

    def test_initialization(self, cache):
        assert cache.cap == 2
        assert len(cache.hm) == 0

    def test_set_and_get(self, cache):
        cache.set("k1", "v1")
        assert cache.get("k1") == "v1"
        assert cache.get("k2") is None

    def test_lru_eviction(self, cache):
        cache.set("k1", "v1")
        cache.set("k2", "v2")
        cache.set("k3", "v3")
        assert cache.get("k1") is None
        assert cache.get("k2") == "v2"
        assert cache.get("k3") == "v3"

    def test_update_existing(self, cache):
        cache.set("k1", "v1")
        cache.set("k1", "v2")
        assert cache.get("k1") == "v2"

    def test_get_reorders(self, cache):
        cache.set("k1", "v1")
        cache.set("k2", "v2")
        cache.get("k1")
        cache.set("k3", "v3")
        assert cache.get("k1") == "v1"
        assert cache.get("k2") is None
        assert cache.get("k3") == "v3"

    def test_edge_cases(self):
        zero_cache = LRUCache(0)
        zero_cache.set("k1", "v1")
        assert zero_cache.get("k1") is None

        one_cache = LRUCache(1)
        one_cache.set("k1", "v1")
        one_cache.set("k2", "v2")
        assert one_cache.get("k1") is None
        assert one_cache.get("k2") == "v2"

        with pytest.raises(ValueError) as excinfo:
            LRUCache(-1)
        assert "Limit must be non-negative!" in str(excinfo.value)
