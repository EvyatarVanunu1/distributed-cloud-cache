from flask_restful import Api

from .cache import CacheResource, CacheData
from .heartbeat import Heartbeat


def register_routes(api: Api):
    api.add_resource(CacheResource, "/cache/<key>")
    api.add_resource(Heartbeat, "/health")
    api.add_resource(CacheData, "/cache-data")
