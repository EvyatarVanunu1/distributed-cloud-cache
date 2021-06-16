import json
import os
import time
import uuid

import boto3

from orchestrator.nodes import NodeClient


def upload_file(bucket, id):

    URL = os.getenv("SERVER_URL")
    sample = {"url": URL, "time": time.time()}
    with open(f'{id}.json', 'w') as fp:
        json.dump(sample, fp)

    s3_client = boto3.client('s3')
    s3_client.upload_file(f'{id}.json', bucket,  f'{id}.json')


if __name__ == '__main__':
    client = NodeClient("my-test-bucket-eidc", "eu-central-1")
    upload_file('my-test-bucket-eidc', uuid.uuid4().hex)

    print(client.get_alive_nodes())
