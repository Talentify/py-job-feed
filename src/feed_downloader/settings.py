import logging.config
import os
from pkgutil import get_data

from yaml import safe_load

# Logging settings
logger_config = get_data("feed_downloader", "config/logger.yaml")
logging.config.dictConfig(safe_load(logger_config))
LOGGER = logging.getLogger("feed_downloader")

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_REGION = os.getenv("AWS_REGION")
AWS_BUCKET = os.getenv("AWS_BUCKET")
