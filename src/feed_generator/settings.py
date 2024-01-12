import os

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