import sys

import click
import xml.etree.ElementTree as ET

from settings import ELASTICSEARCH_INDEX
from src.feed_generator.db import job_feed_config_queries
from src.feed_generator.db.elasticsearch_handler import ElasticSearchHandler


@click.command()
@click.option('--id', type=int, help='ID from table job_feed_config', required=True)
def main(id):
    job_feed_config = job_feed_config_queries.query_by_id(id)
    if not job_feed_config:
        print(f"job_feed_config not found with ID {id}")
        sys.exit(1)

    # Output XML file
    output_file_name = "output.xml"

    # Execute query and save results to XML
    execute_query_and_save_to_xml(ELASTICSEARCH_INDEX, job_feed_config.query, output_file_name)


def execute_query_and_save_to_xml(index, query, output_file):
    # Execute the query
    es = ElasticSearchHandler.get_default().client
    response = es.search(index=index, body=query)

    # Create XML tree
    root = ET.Element("results")

    # Add results to XML
    for hit in response['hits']['hits']:
        result_element = ET.SubElement(root, "result")
        for key, value in hit['_source'].items():
            ET.SubElement(result_element, key).text = str(value)

    # Create and save XML file
    tree = ET.ElementTree(root)
    tree.write(output_file, encoding="utf-8", xml_declaration=True)


if __name__ == "__main__":
    main()
