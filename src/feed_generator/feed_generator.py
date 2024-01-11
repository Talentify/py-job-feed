import sys

import click

from settings import ELASTICSEARCH_INDEX, ELASTICSEARCH_SIZE, ELASTICSEARCH_DEFAULT_SOURCE
from src.feed_generator.db import job_feed_config_queries
from src.feed_generator.db.elasticsearch_handler import ElasticSearchHandler
from src.feed_generator.exporters.xml_exporter import XMLExporter


@click.command()
@click.option('--job-feed-config-id', type=int, help='ID from table job_feed_config', required=True)
def main(job_feed_config_id):
    job_feed_config = job_feed_config_queries.query_by_id(job_feed_config_id)
    if not job_feed_config:
        print(f"job_feed_config not found with ID {job_feed_config_id}")
        sys.exit(1)

    exporter = XMLExporter()
    output_file_name = "output.xml"
    es = ElasticSearchHandler.get_default().client

    response = es.search(
        index=ELASTICSEARCH_INDEX,
        track_total_hits=True,
        source=ELASTICSEARCH_DEFAULT_SOURCE,
        size=ELASTICSEARCH_SIZE,
        query=job_feed_config.query
    )
    print("Got %d Hits:" % response['hits']['total']['value'])

    exporter.export(response, output_file_name)


if __name__ == "__main__":
    main()
