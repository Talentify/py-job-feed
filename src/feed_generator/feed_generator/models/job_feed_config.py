from sqlalchemy import Column, Integer, JSON, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class JobFeedConfig(Base):
    __tablename__ = 'job_feed_config'
    id = Column(Integer, primary_key=True)
    client_id = Column(Integer)
    query = Column(JSON)
    token = Column(String)
