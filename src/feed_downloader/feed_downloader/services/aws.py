import boto3

from feed_downloader.settings import AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY


def get_aws_s3_client():
    s3 = boto3.client('s3', aws_access_key_id=AWS_ACCESS_KEY_ID, aws_secret_access_key=AWS_SECRET_ACCESS_KEY)
    return s3
