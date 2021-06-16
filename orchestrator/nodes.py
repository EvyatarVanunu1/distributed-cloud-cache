import datetime
import json
import typing
from concurrent.futures import ThreadPoolExecutor

import boto3
import requests

endpoint = "cache"


class NodeClient:
    def __init__(self, bucket_name, aws_region):
        self.aws_region = aws_region
        self.bucket_name = bucket_name

    def get_alive_nodes(self) -> typing.List:
        s3 = boto3.resource("s3", region_name=self.aws_region)
        bucket = s3.Bucket(self.bucket_name)

        alive_nodes = []

        for obj in bucket.objects.all():

            body = json.loads(obj.get()["Body"].read())
            if not datetime.datetime.fromtimestamp(body["time"]) < datetime.datetime.now() - datetime.timedelta(seconds=20):
                alive_nodes.append(body["url"])
        return alive_nodes

    def get_key_from_nodes(self, key, nodes):
        futures = []
        with ThreadPoolExecutor() as executor:
            for node in nodes:
                futures.append(executor.submit(self._get_key_from_node, key, node))
            return sorted((future.result() for future in futures), key=lambda cache_item: cache_item.get("time", 0), reverse=True)[0]

    @staticmethod
    def _get_key_from_node(key, node):
        try:
            resp = requests.get(f"{node}/{endpoint}/{key}")
            resp.raise_for_status()
        except requests.RequestException:
            return {}
        return resp.json()

    def put_in_nodes(self, key, val, nodes):
        futures = []
        with ThreadPoolExecutor() as executor:
            for node in nodes:
                futures.append(executor.submit(self._put_in_node, key, val, node))
            return [future for future in futures if future is not None]

    @staticmethod
    def _put_in_node(key, val, node):
        try:
            resp = requests.put(f"{node}/{endpoint}/{key}", json=val)
            resp.raise_for_status()
        except requests.RequestException:
            return None
        return resp.status_code
