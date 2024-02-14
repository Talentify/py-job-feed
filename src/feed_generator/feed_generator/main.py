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
from feed_generator.settings import ELASTICSEARCH_INDEX, ELASTICSEARCH_SCROLL_TIME, ELASTICSEARCH_DEFAULT_SOURCE, \
    FEED_LOCAL_OUTPUT_DIRECTORY, FEED_FORMAT_TYPE, FEED_UPLOAD_TYPE, DELETE_LOCAL_FEED_AFTER_EXECUTION, \
    ELASTICSEARCH_SIZE, FEED_FILE_MAX_RECORDS
from feed_generator.settings import LOGGER as logger


@click.command()
@click.option('--job-feed-config-id', type=int, help='ID from table job_feed_config', required=True)
def main(job_feed_config_id):
    job_feed_config = _search_config(job_feed_config_id)
    if not job_feed_config:
        logger.debug(f"job_feed_config not found with ID {job_feed_config_id}")
        sys.exit(1)

    build_time = datetime.now()

    query = job_feed_config.query

    total_results = _count_job_openings(query)
    logger.debug("Got %d hits" % total_results)

    execution_identifier = build_time.strftime('%Y_%m_%d_%H_%M_%S')
    output_directory = _create_output_directory(job_feed_config_id, execution_identifier)

    feed = FeedFilesManager(
        exporter_class=FEED_FORMAT_TYPE.get_class(),
        output_directory_path=output_directory,
        last_build_date=build_time,
        quantity_of_jobs=total_results
    )

    hits_count = 0
    for hits in _search_job_openings(query, scroll='1m'):
        hits_count += len(hits)
        logger.debug(f"Received {hits_count} hits")
        feed.add_es_hits(hits)
    feed.close()

    if FEED_UPLOAD_TYPE:
        uploader = FEED_UPLOAD_TYPE.get_class()()
        files_prefix = job_feed_config.token
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


def _count_job_openings(query) -> int:
    es = ElasticSearchHandler.get_default().client

    response = es.search(
        index=ELASTICSEARCH_INDEX,
        source=None,
        track_total_hits=True,
        size=0,
        query=query
    )

    count = int(response['hits']['total']['value'])

    return count


def _search_job_openings(query, scroll='1m'):
    es = ElasticSearchHandler.get_default().client

    response = es.search(
        index=ELASTICSEARCH_INDEX,
        source=ELASTICSEARCH_DEFAULT_SOURCE,
        size=ELASTICSEARCH_SIZE,
        scroll=ELASTICSEARCH_SCROLL_TIME,
        query=query
    )

    scroll_id = response['_scroll_id']
    hits = response['hits']['hits']

    while hits:
        yield hits

        response = es.scroll(scroll_id=scroll_id, scroll=scroll)
        scroll_id = response['_scroll_id']
        hits = response['hits']['hits']

    es.clear_scroll(scroll_id=scroll_id)


if __name__ == "__main__":
    main()
