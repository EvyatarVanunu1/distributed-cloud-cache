import itertools

from flask_restful import Resource
from flask import request
from orchestrator.nodes import NodeClient
from ring import Ring


class Cache(Resource):

    def get(self, key):

        client = NodeClient()
        alive_nodes = client.get_alive_nodes()

        ring_nodes = Ring.get_nodes(key=key, nodes=alive_nodes)
        mapped_nodes = Ring.get_nodes_from_map(key=key)

        if mapped_nodes and ring_nodes != mapped_nodes:
            nodes = itertools.chain(mapped_nodes, alive_nodes)
        else:
            nodes = ring_nodes

        return client.get_key_from_nodes(key, nodes), 200

    def put(self, key):

        body = request.get_json() or {}

        if not body.get("data") or not body.get("expiration_date"):
            return {"msg": "invalid request body. missing data or expiration_date attributes"}, 400

        client = NodeClient()
        alive_nodes = client.get_alive_nodes()
        ring_nodes = Ring.get_nodes(key=key, nodes=alive_nodes)









