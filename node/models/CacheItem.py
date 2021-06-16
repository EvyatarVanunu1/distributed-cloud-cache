class CacheItem:
    def __init__(self, key, data, expiration_date, time):
        self.key = key
        self.data = data
        self.expiration_date = expiration_date
        self.time = time

    def serialize(self):
        return {
            "key": self.key,
            "data": self.data,
            "expiration_date": self.expiration_date,
            "time": self.time
        }
