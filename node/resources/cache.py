from flask_restful import Resource
from ..models.Cache import cache
from flask_restful import Resource
from flask import request, current_app



class CacheResource(Resource):
    def get(self, key):
        data = cache.get(key)
        if data:
            return {"data": data}, 200, ({"Content-Type": "application/json"})
        return {}, 200, ({"Content-Type": "application/json"})

    def get(self):
        res = {"cache": []}
        for key, value in cache.items():
            res[cache].append(value.serialize)
        return res, 200, ({"Content-Type": "application/json"})


    def put(self, key):
        body = request.get_json() or dict()

        if not body.get("data") or not body.get("expiration_date") or not body.get("time"):
            return {"msg": "invalid request body. missing data or expiration_date attributes"}, 400
        cache.set(key, body["data"], body["expiration_date"], body["time"])
        return {"msg": "ok"}, 200, ({"Content-Type": "application/json"})
