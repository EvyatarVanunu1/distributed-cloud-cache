import datetime
import time

from flask_restful import Resource
from flask import request, current_app

from node.models.CacheItem import CacheItem
from .nodes import NodeClient
from .ring import Ring, Nodes


class Heartbeat(Resource):

    def get(self):
        return "I'm Alive!", 200


class NodesResource(Resource):

    def get(self):
        return Nodes.get_alive_nodes(), 200


class Cache(Resource):

    def get(self, key):

        client = NodeClient(bucket_name=current_app.config["S3_BUCKET_NAME"], aws_region=current_app.config["AWS_REGION"])
        alive_nodes = Nodes.get_alive_nodes()

        ring_nodes = Ring.get_nodes(key=key, nodes=alive_nodes)
        mapped_nodes = Ring.get_nodes_from_map(key=key)

        if mapped_nodes and ring_nodes != mapped_nodes:
            nodes = mapped_nodes
        else:
            nodes = ring_nodes

        if not nodes:
            return {"msg": "no nodes in the cluster. try to add new nodes"}, 500

        return client.get_key_from_nodes(key, nodes), 200

    def put(self, key):

        body = request.get_json() or {}

        if not body.get("data") or not body.get("expiration_date"):
            return {"msg": "invalid request body. missing data or expiration_date attributes"}, 400

        try:
            expiration_date = datetime.datetime.timestamp(datetime.datetime.fromisoformat(body['expiration_date']))
        except ValueError:
            return 400, {"msg": "invalid expiration_date, should be iso-formatted"}

        cache_item = CacheItem(
            key=key,
            data=body["data"],
            expiration_date=expiration_date,
            time=time.time()
        ).serialize()

        client = NodeClient(bucket_name=current_app.config["S3_BUCKET_NAME"], aws_region=current_app.config["AWS_REGION"])
        alive_nodes = Nodes.get_alive_nodes()
        ring_nodes = Ring.get_nodes(key=key, nodes=alive_nodes)

        resps = client.put_in_nodes(
            key=key,
            val=cache_item,
            nodes=ring_nodes
        )

        if resps:
            Ring.set_to_map(key, nodes=ring_nodes)
            return {}, 200
        else:
            return {"msg": "failed to put data in cache"}, 500


