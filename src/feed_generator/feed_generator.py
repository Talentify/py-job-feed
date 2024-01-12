import os
import sys
from datetime import datetime

import click

from settings import ELASTICSEARCH_INDEX, ELASTICSEARCH_SIZE, ELASTICSEARCH_DEFAULT_SOURCE, FEED_LOCAL_OUTPUT_DIRECTORY
from src.feed_generator.db.elasticsearch_handler import ElasticSearchHandler
from src.feed_generator.db.sqlalchemy_handler import SqlAlchemyHandler
from src.feed_generator.exporters.xml_exporter import XMLExporter

from src.feed_generator.helper.feed_files_manager import FeedFilesManager
from src.feed_generator.models.job_feed_config import JobFeedConfig


@click.command()
@click.option('--job-feed-config-id', type=int, help='ID from table job_feed_config', required=True)
def main(job_feed_config_id):
    job_feed_config = _search_config(job_feed_config_id)
    if not job_feed_config:
        print(f"job_feed_config not found with ID {job_feed_config_id}")
        sys.exit(1)

    execution_identifier = datetime.now().strftime('%Y_%m_%d_%H_%M_%S')

    output_directory = _create_output_directory(job_feed_config_id, execution_identifier)

    feed = FeedFilesManager(XMLExporter, output_directory)

    query = job_feed_config.query

    response = _search_job_openings(query, only_count=True)
    total_results = response['hits']['total']['value']
    print("Got %d Hits:" % total_results)

    _from = 0
    while _from <= total_results:
        print(f"Searching from={_from}")
        response = _search_job_openings(query, from_=_from)
        hits = response['hits']['hits']
        feed.add_es_hits(hits)
        _from += ELASTICSEARCH_SIZE
    feed.close()


def _search_config(job_feed_config_id):
    session = SqlAlchemyHandler.get_default().Session()
    result = session.get(JobFeedConfig, job_feed_config_id)
    session.close()
    return result


def _create_output_directory(job_feed_config_id, execution_identifier):
    output_directory_path = FEED_LOCAL_OUTPUT_DIRECTORY / str(job_feed_config_id) / execution_identifier
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
