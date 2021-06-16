import time
from .CacheItem import CacheItem


class Cache:

    def __init__(self):
        self.map = {}

    def set(self, key, data, expiration_date,time):
        item = CacheItem(key, data, expiration_date, time)
        self.map[key] = item

    def get(self, key):
        item = self.map[key]
        if item:
            if item.expiration_date > time.time():
                self.map.pop(key)
                item = None
        return item


cache = Cache()