#!/usr/bin/python
from google.cloud import storage
storage_client = storage.Client()
bucket = storage_client.get_bucket("pythonvisionapi")
blobs = bucket.list_blobs()
for blob in blobs:
    print(blob.public_url)
