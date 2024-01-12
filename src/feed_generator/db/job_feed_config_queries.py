from src.feed_generator.db.sqlalchemy_handler import SqlAlchemyHandler
from src.feed_generator.models.job_feed_config import JobFeedConfig


def query_by_id(primary_key: int):
    session = SqlAlchemyHandler.get_default().Session()

    result = None
    _exception = None

    try:
        result = session.query(JobFeedConfig).get(primary_key)
        return result

    except Exception as e:
        _exception = e

    finally:
        # Close the session
        session.close()

    if _exception:
        raise _exception
    else:
        return result
