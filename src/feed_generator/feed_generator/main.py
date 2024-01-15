import os
import shutil
import sys
from datetime import datetime
from pathlib import Path

import click

from feed_generator.db.elasticsearch_handler import ElasticSearchHandler
from feed_generator.db.sqlalchemy_handler import SqlAlchemyHandler
from feed_generator.helper.feed_files_manager import FeedFilesManager
from feed_generator.models.job_feed_config import JobFeedConfig
from settings import ELASTICSEARCH_INDEX, ELASTICSEARCH_SIZE, ELASTICSEARCH_DEFAULT_SOURCE, FEED_LOCAL_OUTPUT_DIRECTORY, \
    FEED_FORMAT_TYPE, FEED_UPLOAD_TYPE, DELETE_LOCAL_FEED_AFTER_EXECUTION
from settings import LOGGER as logger


@click.command()
@click.option('--job-feed-config-id', type=int, help='ID from table job_feed_config', required=True)
def main(job_feed_config_id):
    job_feed_config = _search_config(job_feed_config_id)
    if not job_feed_config:
        logger.debug(f"job_feed_config not found with ID {job_feed_config_id}")
        sys.exit(1)

    execution_identifier = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    output_directory = _create_output_directory(job_feed_config_id, execution_identifier)

    feed = FeedFilesManager(FEED_FORMAT_TYPE.get_class(), output_directory)

    query = job_feed_config.query

    response = _search_job_openings(query, only_count=True)
    total_results = response['hits']['total']['value']
    logger.debug("Got %d hits" % total_results)

    _from = 0
    while _from <= total_results:
        logger.debug(f"Searching from={_from}")
        response = _search_job_openings(query, from_=_from)
        hits = response['hits']['hits']
        feed.add_es_hits(hits)
        _from += ELASTICSEARCH_SIZE
    feed.close()

    if FEED_UPLOAD_TYPE:
        uploader = FEED_UPLOAD_TYPE.get_class()()
        files_prefix = str(job_feed_config_id)
        uploader.delete_existing_files(files_prefix=files_prefix)
        uploader.upload_files(origin_path=output_directory, key_prefix=files_prefix)

    if DELETE_LOCAL_FEED_AFTER_EXECUTION:
        shutil.rmtree(output_directory)


def _search_config(job_feed_config_id):
    session = SqlAlchemyHandler.get_default().Session()
    result = session.get(JobFeedConfig, job_feed_config_id)
    session.close()
    return result


def _create_output_directory(job_feed_config_id, execution_identifier):
    output_directory_path = Path(FEED_LOCAL_OUTPUT_DIRECTORY) / str(job_feed_config_id) / execution_identifier
    os.makedirs(output_directory_path)
    return output_directory_path


def _search_job_openings(query, from_=0, only_count=False):
    index = ELASTICSEARCH_INDEX
    if only_count:
        source = None
        track_total_hits = True
        size = 0
    else:
        source = ELASTICSEARCH_DEFAULT_SOURCE
        track_total_hits = False
        size = ELASTICSEARCH_SIZE

    es = ElasticSearchHandler.get_default().client
    response = es.search(
        index=index,
        source=source,
        track_total_hits=track_total_hits,
        size=size,
        query=query,
        from_=from_
    )

    return response


if __name__ == "__main__":
    main()
