import os
from pathlib import Path

import boto3

from src.feed_generator.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_BUCKET


class AwsS3Uploader:

    def __init__(self,
                 aws_access_key_id=AWS_ACCESS_KEY_ID,
                 aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                 aws_region=AWS_REGION):
        self.s3 = boto3.client('s3',
                               aws_access_key_id=aws_access_key_id,
                               aws_secret_access_key=aws_secret_access_key,
                               region_name=aws_region)

    def upload_files(self, origin_path: Path, bucket=AWS_BUCKET, key_prefix: Path = None):
        for root, dirs, files in os.walk(origin_path):
            for file in files:
                file_path = os.path.join(root, file)
                key = os.path.relpath(file_path, origin_path)
                if key_prefix:
                    key = str(os.path.join(key_prefix, key))
                self.upload_file(file_path=file_path, bucket=bucket, key=key)

    def upload_file(self, file_path, key, bucket=AWS_BUCKET):
        try:
            self.s3.upload_file(file_path, bucket, key)
            print(f"File uploaded successfully: {key}")
        except Exception as e:
            print(f"Error uploading file {key}: {str(e)}")
