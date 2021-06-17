import hashlib
import threading
import typing

import jump


class Ring:

    __MAP = {}
    VNODES = 1024

    @classmethod
    def get_nodes(cls, nodes, key):
        vnode = jump.hash(cls._hash_func(key), cls.VNODES)

        if len(nodes) == 0:
            return []
        elif len(nodes) == 1:
            return nodes
        else:
            redundancy = min(max(2, len(nodes) // 4), 4)
            return tuple(set(nodes[(vnode + i) % len(nodes)] for i in range(redundancy)))

    @classmethod
    def get_nodes_from_map(cls, key):
        return cls.__MAP.get(key)

    @classmethod
    def set_to_map(cls, key, nodes: typing.Tuple):
        cls.__MAP[key] = nodes

    @classmethod
    def _hash_func(cls, key):
        return int(hashlib.md5(bytes(key, 'utf-8')).hexdigest(), 16)


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
            cls.__NODES = nodes



