from elasticsearch import Elasticsearch

from feed_generator.settings import ELASTICSEARCH_HOST, ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD


class ElasticSearchHandler:

    _instances = {}

    def __init__(self, host, **kwargs):
        self.client = Elasticsearch([host], **kwargs)

    @classmethod
    def get_instance(cls, host, **kwargs):
        if host not in cls._instances:
            cls._instances[host] = cls(host, **kwargs)
        return cls._instances[host]

    @classmethod
    def get_default(cls):
        host = ELASTICSEARCH_HOST
        auth = (ELASTICSEARCH_USER, ELASTICSEARCH_PASSWORD)
        return cls.get_instance(host, basic_auth=auth)
