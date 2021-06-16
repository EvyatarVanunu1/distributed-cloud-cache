from flask_restful import Api

from .cache import CacheResource
from .heartbeat import Heartbeat


def register_routes(api: Api):
    api.add_resource(CacheResource, "/cache")
    api.add_resource(Heartbeat, "/health")
