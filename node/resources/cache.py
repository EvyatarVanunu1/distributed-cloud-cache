from flask import request
from flask_restful import Resource

from ..models.Cache import cache


class CacheData(Resource):
    def get(self):
        res = {"cache": []}
        for key, value in cache.map.items():
            res["cache"].append(value.serialize())
        return res, 200, ({"Content-Type": "application/json"})


class CacheResource(Resource):
    def get(self, key):
        data = cache.get(key)
        if data:
            return data.serialize(), 200, ({"Content-Type": "application/json"})
        return {}, 200, ({"Content-Type": "application/json"})

    def put(self, key):
        body = request.get_json() or dict()

        if not body.get("data") or not body.get("expiration_date") or not body.get("time"):
            return {"msg": "invalid request body. missing data or expiration_date attributes"}, 400
        cache.set(key, body["data"], body["expiration_date"], body["time"])
        return {"msg": "ok"}, 200, ({"Content-Type": "application/json"})
