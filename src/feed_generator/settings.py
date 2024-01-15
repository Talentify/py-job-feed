import os
from pathlib import Path

from src.feed_generator.exporters.feed_format_type import FeedFormatType
from src.feed_generator.uploaders.feed_upload_type import FeedUploadType

ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST")
ELASTICSEARCH_USER = os.getenv("ELASTICSEARCH_USER")
ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD")
ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX")
ELASTICSEARCH_SIZE = int(os.getenv("ELASTICSEARCH_SIZE"))
ELASTICSEARCH_DEFAULT_SOURCE = (
    [str(elem) for elem in os.getenv("ELASTICSEARCH_DEFAULT_SOURCE").split(",") if elem]
    if os.getenv("ELASTICSEARCH_DEFAULT_SOURCE")
    else []
)

TFLUXV3_CONN_URI = os.getenv("TFLUXV3_CONN_URI")

FEED_FILE_MAX_RECORDS = int(os.getenv("FEED_FILE_MAX_RECORDS"))
FEED_LOCAL_OUTPUT_DIRECTORY = Path(os.getenv("FEED_LOCAL_OUTPUT_DIRECTORY"))

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_BUCKET = os.getenv("AWS_BUCKET")

FEED_FORMAT_TYPE = FeedFormatType(os.getenv("FEED_FORMAT_TYPE"))
FEED_UPLOAD_TYPE = FeedUploadType(os.getenv("FEED_UPLOAD_TYPE")) if os.getenv("FEED_UPLOAD_TYPE") else None
DELETE_LOCAL_FEED_AFTER_EXECUTION = os.getenv("DELETE_LOCAL_FEED_AFTER_EXECUTION", "False").lower() == "true"
