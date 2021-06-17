import datetime
import time
import typing

from .CacheItem import CacheItem


class Cache:

    def __init__(self):
        self.map = {}

    def set(self, key, data, expiration_date, time):
        item = CacheItem(key, data, expiration_date, time)
        self.map[key] = item

    def get(self, key):
        item = self.map.get(key)
        item: typing.Optional[CacheItem]
        if item:
            if time.time() > item.expiration_date:
                self.map.pop(key)
                item = None
        return item


cache = Cache()