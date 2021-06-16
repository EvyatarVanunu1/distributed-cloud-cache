import os
import threading
import time

import flask
from flask_restful import Api

from orchestrator.nodes import NodeClient
from orchestrator.resources import Cache
from orchestrator.ring import Nodes


def update_alive_nodes(bucket_name, region):
    client = NodeClient(bucket_name=bucket_name, aws_region=region)
    while True:
        alive_nodes = client.get_alive_nodes()
        Nodes.set_alive_nodes(alive_nodes)
        time.sleep(5)


def create_app():

    app = flask.Flask(__name__)
    app.config["S3_BUCKET"] = os.getenv("S3_BUCKET")
    app.config["AWS_REGION"] = os.getenv("AWS_REGION")

    api = Api()
    api.add_resource(Cache, "/cache")
    api.init_app(app)

    threading.Thread(target=update_alive_nodes, args=(app.config["S3_BUCKET"], app.config["AWS_REGION"]), daemon=True).start()

    return app

