import hashlib
import threading
import typing

import jump


class Ring:

    __MAP = {}
    VNODES = 1024

    @classmethod
    def get_nodes(cls, nodes, key):
        node = jump.hash(cls._hash_func(key), len(nodes))
        return nodes[node], nodes[(node + 1) % len(nodes)]

    @classmethod
    def get_nodes_from_map(cls, key):
        return cls.__MAP.get(cls._hash_func(key))

    @classmethod
    def set_to_map(cls, key, nodes: typing.Tuple):
        cls.__MAP[cls._hash_func(key)] = nodes

    @classmethod
    def _hash_func(cls, key):
        return int(hashlib.md5(bytes(key, 'utf-8')).hexdigest(), cls.VNODES)


class Nodes:

    __NODES = []
    LOCK = threading.Lock()

    @classmethod
    def get_alive_nodes(cls):
        with cls.LOCK:
            return cls.__NODES

    @classmethod
    def set_alive_nodes(cls, nodes):
        with cls.LOCK:
            __NODES = nodes



