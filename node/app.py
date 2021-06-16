import os
import boto3
import json
import threading
import time
import uuid
from flask import Flask
from flask_restful import Api
from .resources.routes import register_routes


def upload_file(bucket, id):
    while True:
        URL = os.getenv("SERVER_URL")
        sample = {"url": URL, "time": time.time()}
        with open(f'{id}.json', 'w') as fp:
            json.dump(sample, fp)

        s3_client = boto3.client('s3')
        s3_client.upload_file(f'{id}.json', bucket,  f'{id}.json')
        print(f'{id}.json')
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
