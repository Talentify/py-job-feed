import logging.config
import logging.config
import os
from distutils.util import strtobool
from pathlib import Path
from pkgutil import get_data

from yaml import safe_load

from feed_generator.exporters.feed_format_type import FeedFormatType
from feed_generator.uploaders.feed_upload_type import FeedUploadType

# Logging settings
logger_config = get_data("feed_generator", "config/logger.yaml")
logging.config.dictConfig(safe_load(logger_config))
LOGGER = logging.getLogger("feed_generator")

ELASTICSEARCH_HOST = os.getenv("ELASTICSEARCH_HOST")
ELASTICSEARCH_USER = os.getenv("ELASTICSEARCH_USER")
ELASTICSEARCH_PASSWORD = os.getenv("ELASTICSEARCH_PASSWORD")
ELASTICSEARCH_INDEX = os.getenv("ELASTICSEARCH_INDEX")
ELASTICSEARCH_SIZE = int(os.getenv("ELASTICSEARCH_SIZE"))
ELASTICSEARCH_SCROLL_TIME = os.getenv("ELASTICSEARCH_SCROLL_TIME")
ELASTICSEARCH_DEFAULT_SOURCE = (
    [str(elem) for elem in os.getenv("ELASTICSEARCH_DEFAULT_SOURCE").split(",") if elem]
    if os.getenv("ELASTICSEARCH_DEFAULT_SOURCE")
    else []
)

JOBFEED_CONN_URI = os.getenv("JOBFEED_CONN_URI")

FEED_FILE_MAX_RECORDS = int(os.getenv("FEED_FILE_MAX_RECORDS"))
FEED_LOCAL_OUTPUT_DIRECTORY = Path(os.getenv("FEED_LOCAL_OUTPUT_DIRECTORY"))

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_BUCKET = os.getenv("AWS_BUCKET")

FEED_FORMAT_TYPE = FeedFormatType(os.getenv("FEED_FORMAT_TYPE"))
FEED_UPLOAD_TYPE = FeedUploadType(os.getenv("FEED_UPLOAD_TYPE")) if os.getenv("FEED_UPLOAD_TYPE") else None
DELETE_LOCAL_FEED_AFTER_EXECUTION = bool(strtobool(os.getenv("DELETE_LOCAL_FEED_AFTER_EXECUTION")))
