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
    es = ElasticSearchHandler.get_default().client

    ffb = FeedFilesBuilder(XMLHandler, output_file_name)

    query = job_feed_config.query

    page_size = ELASTICSEARCH_SIZE

    current_page = 1

    response = _search_job_openings(query, track_total_hits=True)
    total_results = response['hits']['total']['value']
    hits = response['hits']['hits']
    print("Got %d Hits:" % total_results)
    ffb.append_results(hits)
    while current_page * page_size <= total_results:
        start_index = current_page * page_size
        print(f"Searching start_index={start_index}")
        response = _search_job_openings(query, from_=start_index)
        hits = response['hits']['hits']
        ffb.append_results(hits)
        current_page += 1
    ffb.close()


def _search_job_openings(query, from_=0, track_total_hits=False):
    es = ElasticSearchHandler.get_default().client
    response = es.search(
        index=ELASTICSEARCH_INDEX,
        track_total_hits=track_total_hits,
        source=ELASTICSEARCH_DEFAULT_SOURCE,
        size=ELASTICSEARCH_SIZE,
        query=query,
        from_=from_
    )


    return response


if __name__ == "__main__":
    main()
