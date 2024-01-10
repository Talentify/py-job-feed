from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class SqlAlchemyHandler:
    _instances = {}

    def __new__(cls, connection_string):
        if connection_string not in cls._instances:
            cls._instances[connection_string] = super().__new__(cls)
            cls._instances[connection_string].engine = create_engine(connection_string)
            cls._instances[connection_string].Session = sessionmaker(bind=cls._instances[connection_string].engine)
        return cls._instances[connection_string]
