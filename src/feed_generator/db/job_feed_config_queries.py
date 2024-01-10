from src.feed_generator.db.database_handler import DatabaseHandler
from src.feed_generator.models.job_feed_config import JobFeedConfig
from src.feed_generator.settings import TFLUXV3_CONN_URI


def query_by_id(primary_key: int):
    handler = DatabaseHandler(TFLUXV3_CONN_URI)
    session = handler.Session()

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
