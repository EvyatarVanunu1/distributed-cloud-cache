import datetime
import logging
import os
import sys
from logging import getLogger
import boto3
import json
import threading
import time
import uuid
from flask import Flask
from flask_restful import Api
from .resources.routes import register_routes

logger = getLogger(__name__)
logger.setLevel(logging.INFO)
handler = logging.StreamHandler(sys.stdout)
handler.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


def get_server_url():
    return f"{os.getenv('SERVER_URL')}:{os.getenv('NODE_PORT', 80)}"


def upload_file(bucket, id):
    while True:
        url = get_server_url()
        sample = {"url": url, "time": time.time()}
        with open(f'{id}.json', 'w') as fp:
            json.dump(sample, fp)

        s3_client = boto3.client('s3')
        logger.info(f'trying to upload {id}.json')
        s3_client.upload_file(f'{id}.json', bucket,  f'{id}.json')
        logger.info(f'{id}.json')
        time.sleep(5)


def create_app():

    app = Flask(__name__)
    api = Api()
    register_routes(api)
    api.init_app(app)

    id = str(uuid.uuid4())
    BUCKET = os.getenv("S3_BUCKET_NAME")

    t = threading.Thread(target=upload_file, args=(BUCKET, id), daemon=True)
    t.start()
    return app


if __name__ == "__main__":
    app = create_app()
    app.run(host="0.0.0.0")
