from flask_restful import Api

from .cache import CacheResource


def register_routes(api: Api):
    api.add_resource(CacheResource, "/cache")
