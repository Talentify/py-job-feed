import os
from pathlib import Path

import boto3

from feed_generator.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_REGION, AWS_BUCKET


class AwsS3Uploader:

    def __init__(self,
                 aws_access_key_id=AWS_ACCESS_KEY_ID,
                 aws_secret_access_key=AWS_SECRET_ACCESS_KEY,
                 aws_region=AWS_REGION):
        self.s3 = boto3.client('s3',
                               aws_access_key_id=aws_access_key_id,
                               aws_secret_access_key=aws_secret_access_key,
                               region_name=aws_region)

    def delete_existing_files(self, files_prefix, bucket_name=AWS_BUCKET):
        # List objects in the bucket with the given prefix
        response = self.s3.list_objects_v2(Bucket=bucket_name, Prefix=files_prefix)

        # Check if there are any objects to delete
        if 'Contents' in response:
            # Create a list of objects to delete
            objects_to_delete = [{'Key': obj['Key']} for obj in response['Contents']]

            # Delete objects
            self.s3.delete_objects(Bucket=bucket_name, Delete={'Objects': objects_to_delete})

            print(f"Deleted {len(objects_to_delete)} objects with prefix '{files_prefix}' in bucket '{bucket_name}'")
        else:
            print(f"No objects found with prefix '{files_prefix}' in bucket '{bucket_name}'")

    def upload_files(self, origin_path: Path, bucket=AWS_BUCKET, key_prefix: str = None):
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
