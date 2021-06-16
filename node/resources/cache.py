from flask_restful import Resource
from node.models.Cache import Cache


class Cache(Resource):
    def get(self, key):
        data = Cache.cache.get(key)
        if data:
            return {"data": data}, 200, ({"Content-Type": "application/json"})
        return {}, 200, ({"Content-Type": "application/json"})

    def put(self, key, data, expiration_date, time):
        Cache.cache.set(key, data, expiration_date, time)
        return {"msg": "ok"}, 200, ({"Content-Type": "application/json"})
