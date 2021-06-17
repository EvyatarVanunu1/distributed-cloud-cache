import datetime
import os
import threading
import time
from logging import getLogger

import flask
from flask_restful import Api

from orchestrator.nodes import NodeClient
from orchestrator.resources import Cache, Heartbeat, NodesResource
from orchestrator.ring import Nodes

logger = getLogger(__name__)


def update_alive_nodes(bucket_name, region):
    client = NodeClient(bucket_name=bucket_name, aws_region=region)
    while True:
        logger.info(f"fetching alive nodes {datetime.datetime.now().isoformat()}")
        alive_nodes = client.get_alive_nodes()
        Nodes.set_alive_nodes(alive_nodes)
        logger.info(f"alive nodes {alive_nodes}-{datetime.datetime.now().isoformat()}")
        time.sleep(5)


def create_app():

    app = flask.Flask(__name__)
    app.config["S3_BUCKET_NAME"] = os.getenv("S3_BUCKET_NAME")
    app.config["AWS_REGION"] = os.getenv("AWS_REGION")

    api = Api()
    api.add_resource(Cache, "/cache/<key>")
    api.add_resource(Heartbeat, "/health")
    api.add_resource(NodesResource, "/nodes")
    api.init_app(app)

    threading.Thread(target=update_alive_nodes, args=(app.config["S3_BUCKET_NAME"], app.config["AWS_REGION"]), daemon=True).start()

    return app

