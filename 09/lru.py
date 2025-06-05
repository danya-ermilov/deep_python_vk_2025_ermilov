import sys
import logging
import argparse
from collections import abc
from typing import Hashable, Any


class Node:
    def __init__(self, key: Hashable = -1, val: Any = -1):
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

    def append(self, node: Node) -> None:
        left, right = self.finish.prev, self.finish
        left.next = node
        node.next = right
        node.prev = left
        right.prev = node

    def delete(self, node: Node) -> Node:
        left, right = node.prev, node.next
        left.next = right
        right.prev = left
        return node

    def move_to_finish(self, node: Node) -> None:
        self.append(self.delete(node))

    def popleft(self) -> Node:
        return self.delete(self.start.next)


class LRUCache:
    def __init__(self, log_name: str, limit: int = 4):
        self.hm = {}
        self.dll = DLL()
        self.cap = limit
        self.logger = logging.getLogger(log_name)

        if not isinstance(self.cap, int) or self.cap <= 0:
            self.logger.critical(
                "Invalid cache limit: %s (type: %s). Must be positive integer",
                limit,
                type(limit),
            )
            raise ValueError("Limit must be positive integer")

    def get(self, key: Hashable) -> Any:
        if not isinstance(key, abc.Hashable):
            self.logger.error("Non-hashable key provided: %s (type: %s)", key, type(key))
            raise TypeError("Key must be hashable")

        if key not in self.hm:
            self.logger.info("Key not found: %s", key)
            return None

        node = self.hm[key]
        self.dll.move_to_finish(node)
        self.logger.debug("Retrieved key: %s -> value: %s", key, node.val)
        return node.val

    def set(self, key: Hashable, value: Any) -> None:
        if not isinstance(key, abc.Hashable):
            self.logger.error("Non-hashable key provided: %s (type: %s)", key, type(key))
            raise TypeError("Key must be hashable")

        if key in self.hm:
            self.logger.info("Updating existing key: %s", key)
            node = self.dll.delete(self.hm[key])
            node.val = value
        else:
            self.logger.info("Adding new key: %s", key)
            node = Node(key, value)
            self.hm[key] = node

        self.dll.append(node)

        if len(self.hm) > self.cap:
            removed = self.dll.popleft()
            self.logger.warning(
                "Cache full (%s/%s). Evicted key: %s",
                len(self.hm),
                self.cap,
                removed.key,
            )
            self.hm.pop(removed.key)


class OddWordsFilter(logging.Filter):
    def filter(self, record):
        return len(record.getMessage().split()) % 2 != 0


def parse_args() -> tuple[bool, bool]:
    parser = argparse.ArgumentParser(description='LRU Cache with logging')
    parser.add_argument(
        '-s',
        action='store_true',
        help='Enable logging to stdout',
    )
    parser.add_argument(
        '-f',
        action='store_true',
        help='Apply custom filter to stdout logs',
    )
    return parser.parse_args().s, parser.parse_args().f


def setup_logging(in_stdout: bool, add_filter: bool) -> str:
    logger_name = 'lru_cache'
    logger = logging.getLogger(logger_name)
    logger.setLevel(logging.DEBUG)

    for handler in logger.handlers[:]:
        logger.removeHandler(handler)
        handler.close()

    file_handler = logging.FileHandler("/mnt/c/users/dell/desktop/deep_python_vk_2025_ermilov/09/cache.log", mode="w")
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)
    logger.addHandler(file_handler)

    if in_stdout:
        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setLevel(logging.DEBUG)
        stdout_formatter = logging.Formatter('[%(levelname)s] %(message)s')
        stdout_handler.setFormatter(stdout_formatter)

        if add_filter:
            stdout_handler.addFilter(OddWordsFilter())

        logger.addHandler(stdout_handler)

    return logger_name


def main():
    stdout_logging, use_filter = parse_args()
    logger_name = setup_logging(stdout_logging, use_filter)

    cache = LRUCache(log_name=logger_name, limit=2)

    operations = [
        ('set', 'k1', 'val1'),
        ('set', 'k2', 'val2'),
        ('get', 'k3'),
        ('get', 'k2'),
        ('get', 'k1'),
        ('set', 'k3', 'val3'),
        ('get', 'k3'),
        ('get', 'k2'),
        ('get', 'k1'),
        ('get', 'k4'),
    ]

    for op, *args in operations:
        try:
            if op == 'set':
                cache.set(*args)
            elif op == 'get':
                cache.get(*args)
        except Exception as e:
            logging.getLogger(logger_name).exception("Operation failed: %s %s", op, args)


if __name__ == "__main__":
    main()
