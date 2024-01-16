import logging.config
import os
from distutils.util import strtobool
from pkgutil import get_data

from yaml import safe_load

DEBUG = bool(strtobool(os.getenv("DEBUG")))

# Logging settings
logger_config = get_data("feed_downloader", "config/logger.yaml")
logging.config.dictConfig(safe_load(logger_config))
LOGGER = logging.getLogger("feed_downloader")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_BUCKET = os.getenv("AWS_BUCKET")

APP_HOST = os.getenv("APP_HOST")
APP_PORT = os.getenv("APP_PORT")

FEED_DOWNLOAD_CHUNK_SIZE = int(os.getenv("FEED_DOWNLOAD_CHUNK_SIZE"))
