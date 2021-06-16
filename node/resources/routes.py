from flask_restful import Api

from .cache import Cache


def register_routes(api: Api):
    api.add_resource(Cache, "/cache")