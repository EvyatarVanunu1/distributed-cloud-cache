from flask_restful import Resource


class Cache(Resource):
    def get(self, key):

            return {"data": None}, 200, ({"Content-Type": "application/json"})

    def put(self, key, data, expiration_date):

        return {"data": None}, 200, ({"Content-Type": "application/json"})
