import sys

import click

from settings import ELASTICSEARCH_INDEX, ELASTICSEARCH_SIZE, ELASTICSEARCH_DEFAULT_SOURCE
from src.feed_generator.db import job_feed_config_queries
from src.feed_generator.db.elasticsearch_handler import ElasticSearchHandler
from src.feed_generator.exporters.feed_files_builder import FeedFilesBuilder

from src.feed_generator.exporters.formats.xml_handler import XMLHandler


@click.command()
@click.option('--job-feed-config-id', type=int, help='ID from table job_feed_config', required=True)
def main(job_feed_config_id):
    job_feed_config = job_feed_config_queries.query_by_id(job_feed_config_id)
    if not job_feed_config:
        print(f"job_feed_config not found with ID {job_feed_config_id}")
        sys.exit(1)

    output_file_name = "output.xml"

    ffb = FeedFilesBuilder(XMLHandler, output_file_name)

    query = job_feed_config.query

    response = _search_job_openings(query, only_count=True)
    total_results = response['hits']['total']['value']
    print("Got %d Hits:" % total_results)

    _from = 0
    while _from <= total_results:
        print(f"Searching from={_from}")
        response = _search_job_openings(query, from_=_from)
        hits = response['hits']['hits']
        ffb.append_results(hits)
        _from += ELASTICSEARCH_SIZE
    ffb.close()


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
