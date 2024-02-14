from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from feed_generator.settings import JOBFEED_CONN_URI


class SqlAlchemyHandler:

    _instances = {}

    def __init__(self, connection_string):
        self.engine = create_engine(connection_string)
        self.Session = sessionmaker(bind=self.engine)

    @classmethod
    def get_instance(cls, connection_string):
        if connection_string not in cls._instances:
            cls._instances[connection_string] = cls(connection_string)
        return cls._instances[connection_string]

    @classmethod
    def get_default(cls):
        return cls.get_instance(JOBFEED_CONN_URI)
